# Generated by Django 5.1.3 on 2024-11-30 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=50)),
                ('address', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('inventory_id', models.AutoField(primary_key=True, serialize=False)),
                ('batch_id', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('manufacturing_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('mfg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField(blank=True, null=True)),
                ('contact', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('med_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('safe_stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ReturnPolicy',
            fields=[
                ('return_id', models.AutoField(primary_key=True, serialize=False)),
                ('thresh_days', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Salt',
            fields=[
                ('salt_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('max_qty', models.IntegerField()),
                ('prescription', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supplier_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('bill_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='pharma.customer')),
            ],
        ),
        migrations.CreateModel(
            name='BillInvoice',
            fields=[
                ('bill_invoice_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='pharma.bill')),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_invoices', to='pharma.inventory')),
            ],
        ),
        migrations.AddField(
            model_name='inventory',
            name='med',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='pharma.medicine'),
        ),
        migrations.CreateModel(
            name='MedMfg',
            fields=[
                ('med_mfg_id', models.AutoField(primary_key=True, serialize=False)),
                ('med', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturers', to='pharma.medicine')),
                ('mfg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='pharma.manufacturer')),
            ],
        ),
        migrations.AddField(
            model_name='medicine',
            name='salt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='pharma.salt'),
        ),
        migrations.CreateModel(
            name='MedicineSupplier',
            fields=[
                ('medicine_supplier_id', models.AutoField(primary_key=True, serialize=False)),
                ('med', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='pharma.medicine')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='pharma.supplier')),
            ],
        ),
        migrations.AddField(
            model_name='inventory',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='pharma.supplier'),
        ),
        migrations.CreateModel(
            name='SupplierReference',
            fields=[
                ('supplier_ref_id', models.AutoField(primary_key=True, serialize=False)),
                ('return_policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_references', to='pharma.returnpolicy')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='references', to='pharma.supplier')),
            ],
        ),
    ]
