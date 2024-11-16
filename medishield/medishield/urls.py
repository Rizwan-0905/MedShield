"""
URL configuration for medishield project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),# done
    path('suppliers/',views.suppliers,name='suppliers'), #done
    path('new_supp/',views.new_supp,name='new_supp'),#done
    path('bills/',views.bill,name='bills'),#done
    path('add_bill/',views.add_bill,name='add_bill'),#done
    path('dead_stock/',views.dead_stock,name='dead_stock'),#done
    path('customers/',views.customer,name='customer'),# done
    path('orders/',views.orders,name='orders'),#done
    path('add_order/',views.add_order,name='add_order'),
    path('receive_order/',views.receive_order,name='receive_order'),# deal with inventory upon receiving order
    path('inventory/',views.inventory,name='inventory'),#done
    path('returns/',views.returns,name='returns'),
     path('add_return/',views.add_return,name='add_return'),
    path('complete_returns/',views.complete_returns,name='complete_returns')

]
