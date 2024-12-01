from django.contrib import admin
from .models import Manufacturer, Salt, Medicine, MedMfg, Supplier, MedicineSupplier, ReturnPolicy, SupplierReference, Customer, Bill, Inventory, BillInvoice

admin.site.register(Manufacturer)
admin.site.register(Salt)
admin.site.register(Medicine)
admin.site.register(MedMfg)
admin.site.register(Supplier)
admin.site.register(MedicineSupplier)
admin.site.register(ReturnPolicy)
admin.site.register(SupplierReference)
admin.site.register(Customer)
admin.site.register(Bill)
admin.site.register(Inventory)
admin.site.register(BillInvoice)
