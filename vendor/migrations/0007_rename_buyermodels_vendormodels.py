# Generated by Django 3.2.9 on 2021-12-09 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211209_1341'),
        ('vendor', '0006_buyermodels_emails_menufactures'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BuyerModels',
            new_name='VendorModels',
        ),
    ]
