# created by Rizwan
from django.http import HttpResponse
from django.shortcuts import render
import datetime

def home(request):
    x=datetime.datetime.now()
    params={'date':x}
    return render(request,'home.html',params)




# Suppliers page view
def suppliers(request):
    return render(request, 'suppliers.html')

# Add new supplier view
def new_supp(request):
    return render(request, 'new_supp.html')

def add_return(request):
    return render(request, 'add_return.html')

# Bills page view
def bill(request):
    return render(request, 'bills.html')

# Add a new bill view
def add_bill(request):
    return render(request, 'add_bill.html')

# Dead stock page view
def dead_stock(request):
    return render(request, 'dead_stock.html')

# Customers page view
def customer(request):
    return render(request, 'customers.html')



# Orders page view
def orders(request):
    return render(request, 'orders.html')

# Add a new order view
def add_order(request):
    return render(request, 'add_order.html')

# Receive an order view
def receive_order(request):
    return render(request, 'receive_order.html')

# Inventory page view
def inventory(request):
    return render(request, 'inventory.html')

# Returns page view
def returns(request):
    return render(request, 'returns.html')

# Complete returns page view
def complete_returns(request):
    return render(request, 'complete_returns.html')
