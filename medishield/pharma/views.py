# created by Rizwan
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from .models import Customer,Inventory,Medicine,Supplier,Bill,BillInvoice
from django.db import connection,transaction
from decimal import Decimal
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import transaction, connection
from .models import Customer, Bill, BillInvoice, Inventory, Salt
from decimal import Decimal
from datetime import datetime


def home(request):
    x=datetime.datetime.now()
    params={'date':x}
    return render(request,'pharma/home.html',params)




# Suppliers page view
def suppliers(request):
    
    return render(request, 'pharma/suppliers.html')

# Add new supplier view
def new_supp(request):
    return render(request, 'pharma/new_supp.html')

def add_return(request):
    return render(request, 'pharma/add_return.html')

# Bills page view
def bill(request):
    return render(request, 'pharma/bills.html')

# Add a new bill view
from django.db import transaction, connection
from datetime import datetime
from decimal import Decimal

from django.db import transaction
from datetime import datetime
from decimal import Decimal

from django.db import transaction, IntegrityError
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
            inventory_ids = request.POST.getlist('inventory_id[]')
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
            bill_date = datetime.today().date()
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


# Dead stock page view
def dead_stock(request):
    return render(request, 'pharma/dead_stock.html')

# Customers page view
def customer(request):
    #customs=Customer.objects.raw("select * from Customer")
    customs=Customer.objects.all()
    context = {'customers': customs}
    return render(request, 'pharma/customers.html',context)


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

def add_inv(request):
    
    return render(request, "pharma/add_inv.html")


# Returns page view
def returns(request):
    return render(request, 'pharma/returns.html')

# Complete returns page view
def complete_returns(request):
    return render(request, 'pharma/complete_returns.html')


