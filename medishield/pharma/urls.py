from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('', views.home, name='home'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('individ_bill/', views.individ_bill, name='individ_bill'),  # Supplier list
    path('new_supp/', views.new_supp, name='new_supp'),  # Add new supplier
    path('bills/', views.bill, name='bills'),  # Bill list
    path('add_bill/', views.add_bill, name='add_bill'),  # Add new bill
    path('dead_stock/', views.dead_stock, name='dead_stock'),  # Dead stock
    path('customers/', views.customer, name='customer'),  # Customer list
    path('add_customer/', views.add_customer, name='add_customer'),
    path('inventory/', views.inventory, name='inventory'),  # Inventory management
    path('add_inv/', views.add_inv, name='add_inv'),
    path('returns/', views.returns, name='returns'),  # Returns list
    path('add_return/', views.add_return, name='add_return'),  # Add return
  # Complete returns
]
