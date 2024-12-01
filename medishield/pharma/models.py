from django.db import models



class Manufacturer(models.Model):
    mfg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Salt(models.Model):
    salt_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    max_qty = models.IntegerField()
    prescription = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    med_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    safe_stock = models.IntegerField()
    salt = models.ForeignKey(Salt, on_delete=models.CASCADE, related_name="medicines")

    def __str__(self):
        return self.name


class MedMfg(models.Model):
    med_mfg_id = models.AutoField(primary_key=True)
    med = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="manufacturers")
    mfg = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="medicines")

    def __str__(self):
        return f"{self.med.name} - {self.mfg.name}"


class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MedicineSupplier(models.Model):
    medicine_supplier_id = models.AutoField(primary_key=True)
    med = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="suppliers")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="medicines")

    def __str__(self):
        return f"{self.med.name} - {self.supplier.name}"


class ReturnPolicy(models.Model):
    return_id = models.AutoField(primary_key=True)
    thresh_days = models.IntegerField()

    def __str__(self):
        return f"Return Policy {self.return_id} - {self.thresh_days} days"




class SupplierReference(models.Model):
    supplier_ref_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="references")
    return_policy = models.ForeignKey(ReturnPolicy, on_delete=models.CASCADE, related_name="supplier_references")

    def __str__(self):
        return f"{self.supplier.name} - Return Policy {self.return_policy.return_id}"


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    last_purch=models.DateField(null=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bills")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date=models.DateField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Bill {self.bill_id} for {self.customer.name}"


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    med = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="inventory")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="inventory")
    batch_id = models.CharField(max_length=50)
    quantity = models.IntegerField()
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Inventory {self.inventory_id} - {self.med.name}"

class Returns(models.Model):
    r_id=models.AutoField(primary_key=True)
    inv_id=models.ForeignKey(Inventory,on_delete=models.CASCADE,related_name="return_inventory")
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE, related_name="ret_suppl")
    qty=models.IntegerField(max_length=7)

class BillInvoice(models.Model):
    bill_invoice_id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="invoices")
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="bill_invoices")
    quantity = models.IntegerField()

    def __str__(self):
        return f"Invoice {self.bill_invoice_id} for Bill {self.bill.bill_id}"
