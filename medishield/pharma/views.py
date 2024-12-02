# created by Rizwan
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate
from django.contrib import messages
import json
from django.http import JsonResponse
from .models import Customer,Inventory,Medicine,Supplier,Bill,BillInvoice,Returns
from django.db import connection,transaction
from decimal import Decimal
import datetime 
from datetime import date
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import transaction, connection
from .models import Customer, Bill, BillInvoice, Inventory, Salt
from decimal import Decimal
from django.db import transaction, IntegrityError




def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login( request,user)  # Log the user in
            messages.success(request, "Welcome back, " + username + "!")
            return redirect('home')  # Redirect to home or dashboard
        else:
            # Add error message for invalid credentials
            messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, 'pharma/login.html')
from django.contrib.auth.decorators import login_required

# Use the login_required decorator on each view that requires authentication

@login_required
def home(request):
    x = datetime.datetime.now()
    params = {'date': x}
    return render(request, 'pharma/home.html', params)

from django.shortcuts import render
from .models import Bill, BillInvoice, Inventory, Medicine

def individ_bill(request):
    # Get the bill ID from the GET parameter
    bill_id = request.GET.get('bill_id')
    
    # Retrieve the bill and related invoice data, including inventory details and associated medicines
    bill = Bill.objects.get(bill_id=bill_id)
    invoices = BillInvoice.objects.filter(bill_id=bill_id).select_related('inventory')
    
    # Prepare a list to hold the data including medicine name and total price for each item
    invoices_with_total = []
    for invoice in invoices:
        medicine_name = invoice.inventory.med.name  # Access the related medicine name
        total_price = invoice.quantity * invoice.inventory.sell_price  # Calculate total price
        
        invoices_with_total.append({
            'invoice': invoice,
            'medicine_name': medicine_name,
            'total_price': total_price
        })
    
    # Prepare the context
    context = {
        'bill': bill,
        'invoices_with_total': invoices_with_total,
    }
    
    return render(request, 'pharma/individ_bill.html', context)



@login_required
def suppliers(request):
    return render(request, 'pharma/suppliers.html')

@login_required
def new_supp(request):
    return render(request, 'pharma/new_supp.html')

@login_required
def add_return(request):
    inv = Inventory.objects.all()
    inv_data = [
        {
            'id': item.inventory_id,
            'med': item.med.name,
            'supplier': item.supplier.name,
            'buy_price': float(item.buy_price),  # Convert Decimal to float
            'quantity': item.quantity
        } 
        for item in inv
    ]
    
    data = {
        'inv_json': json.dumps(inv_data),  # Serialize data to JSON
        'inv': inv
    }

    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id')
        qty_returned = request.POST.get('qty_returned')

        try:
            inventory = Inventory.objects.get(inventory_id=inventory_id)

            # Validate quantity
            if int(qty_returned) > inventory.quantity:
                data['error'] = "Return quantity cannot exceed inventory quantity."
            else:
                # Process the return
                inventory.quantity -= int(qty_returned)
                inventory.save()
                data['message'] = "Return processed successfully."
                return redirect('inventory')
        except Inventory.DoesNotExist:
            data['error'] = "Invalid Inventory ID."

    return render(request, 'pharma/add_return.html', data)

def fetch_inventory(request):
    """API endpoint to fetch inventory data by ID."""
    inventory_id = request.GET.get('inventory_id')

    try:
        inventory = Inventory.objects.get(id=inventory_id)
        response_data = {
            'medicine_name': inventory.med.name,
            'supplier': inventory.supplier.name,
            'purchase_price': inventory.buy_price,
            'quantity': inventory.quantity,
        }
        return JsonResponse(response_data)
    except Inventory.DoesNotExist:
        return JsonResponse({'error': 'Inventory not found.'}, status=404)

@login_required
def bill(request):
    bill = Bill.objects.raw("select * from all_bills")
    params = {'data': bill}
    return render(request, 'pharma/bills.html', params)

@login_required
def add_bill(request):
    # Fetch inventory using raw SQL query
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM all_inventory")
        columns = [col[0] for col in cursor.description]
        inventory = [dict(zip(columns, row)) for row in cursor.fetchall() if len(row) == len(columns)]

    if request.method == 'POST':
        print(request.POST)
        try:
            customer_name = request.POST.get('customerName')
            customer_contact = request.POST.get('customerContact')
            print(f"Received Customer Data: {customer_name}, {customer_contact}")

            customer, created = Customer.objects.get_or_create(
                contact=customer_contact,
                defaults={'name': customer_name}
            )
            print(f"Customer: {customer.name}, Created: {created}")

            # Step 3: Retrieve medicines and quantities from the form data
            inventory_ids = request.POST.getlist('item_id[]')
            quantities = request.POST.getlist('quantity[]')
            total_amount = request.POST.get('totalAmount', 0.0)

            description_needed = False

            # Step 4: Validate quantities and check if a description is needed
            for inventory_id, qty in zip(inventory_ids, quantities):
                inventory_item = Inventory.objects.get(inventory_id=inventory_id)
                salt = inventory_item.med.salt
                max_qty = salt.max_qty

                if int(qty) > max_qty:
                    return JsonResponse({'error': f"Cannot sell more than {max_qty} units of {inventory_item.med.name}."}, status=400)

                if salt.prescription:
                    description_needed = True

            # Step 5: Create a Bill record
            bill_date = date.today()
            bill = Bill.objects.create(
                customer=customer,
                total_amount=total_amount,
                date=bill_date
            )
            print(f"Bill Created: {bill.bill_id}, Total Amount: {bill.total_amount}")

            # Step 6: Process each medicine in the sale (create BillInvoice and update Inventory)
            with transaction.atomic():  # Begin a transaction
                for inventory_id, qty in zip(inventory_ids, quantities):
                    inventory_item = Inventory.objects.get(inventory_id=inventory_id)
                    print(f"h{inventory_item} :")
                    if inventory_item.quantity >= int(qty):

                        inventory_item.quantity -= int(qty)
                        inventory_item.save()
                        print(f"Updated Inventory {inventory_item.inventory_id}: {inventory_item.quantity} remaining.")


                        BillInvoice.objects.create(
                            bill=bill,
                            inventory=inventory_item,
                            quantity=qty
                        )
                        print(f"Created BillInvoice for Bill {bill.bill_id} with Inventory ID {inventory_item.inventory_id} and Quantity {qty}.")
                    else:
                        raise ValueError(f"Not enough stock for {inventory_item.med.name}.")

                customer.last_purch = bill_date
                customer.save()
                print(f"Customer {customer.name}'s last purchase date updated to {customer.last_purch}.")

        except IntegrityError as e:
            print(f"Transaction failed: {e}")
            return JsonResponse({'error': "Database transaction failed. Please try again."}, status=400)

        except ValueError as e:
            print(f"Validation error: {e}")
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'error': "An unexpected error occurred. Please contact support."}, status=500)

 
        if description_needed:
            return JsonResponse({'message': 'A prescription is required for some of the medicines in the bill.'}, status=200)

        return redirect('bills')

 
    return render(request, 'pharma/add_bill.html', {'inventory': inventory})



@login_required
def dead_stock(request):
    return render(request, 'pharma/dead_stock.html')

@login_required
def customer(request):
    customs = Customer.objects.all()
    context = {'customers': customs}
    return render(request, 'pharma/customers.html', context)

@login_required
def add_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')

        existing_customer = Customer.objects.filter(contact=contact).first()

        if existing_customer:
            error_message = "A customer with this contact number already exists."
            return render(request, 'pharma/add_customer.html', {'error': error_message})

        new_customer = Customer(name=name, contact=contact, address=address)
        new_customer.save()
        return redirect('customer')

    return render(request, 'pharma/add_customer.html')

@login_required
def inventory(request):
    if request.method == "POST":
        # Process form data
        try:
            med_id = request.POST.get("med_id")
            supplier_id = request.POST.get("supplier_id")
            batch_id = request.POST.get("batch_id")
            quantity = request.POST.get("quantity")
            manufacturing_date = request.POST.get("manufacturing_date")
            expiry_date = request.POST.get("expiry_date")
            buy_price = request.POST.get("buy_price")
            sell_price = request.POST.get("sell_price")

            # Validate and save
            med = Medicine.objects.get(med_id=med_id)
            supplier = Supplier.objects.get(supplier_id=supplier_id)

            inventory = Inventory(
                med=med,
                supplier=supplier,
                batch_id=batch_id,
                quantity=int(quantity),
                manufacturing_date=manufacturing_date,
                expiry_date=expiry_date,
                buy_price=float(buy_price),
                sell_price=float(sell_price),
            )
            inventory.save()

            # Flash success message
            messages.success(request, "Inventory added successfully!")
            return redirect("inventory")  # Replace with your inventory page URL
        except Medicine.DoesNotExist:
            messages.error(request, "Invalid Medicine ID.")
        except Supplier.DoesNotExist:
            messages.error(request, "Invalid Supplier ID.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    # Fetch inventory data for GET request
    inv = Inventory.objects.raw("SELECT * FROM all_inventory")
    context = {'data': inv}
    return render(request, "pharma/inventory.html", context)

@login_required
def add_inv(request):
    return render(request, "pharma/add_inv.html")

@login_required
def returns(request):
    dead_stock = Inventory.objects.raw("select * from dead_stock")
    return render(request, 'pharma/returns.html', {'returns': dead_stock})
