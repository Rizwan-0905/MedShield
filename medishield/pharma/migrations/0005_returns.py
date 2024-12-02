# Generated by Django 5.1.3 on 2024-11-30 18:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharma', '0004_alter_customer_last_purch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Returns',
            fields=[
                ('r_id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField(max_length=7)),
                ('inv_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_inventory', to='pharma.inventory')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ret_suppl', to='pharma.supplier')),
            ],
        ),
    ]