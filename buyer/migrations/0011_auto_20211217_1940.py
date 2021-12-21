# Generated by Django 3.2.9 on 2021-12-17 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0010_buyerinquiry_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyerinquirytovendor',
            old_name='creation_datetime',
            new_name='no_of_vendor_send',
        ),
        migrations.RenameField(
            model_name='buyerinquirytovendor',
            old_name='inquires',
            new_name='quotes_received',
        ),
        migrations.RemoveField(
            model_name='buyerinquirytovendor',
            name='created_by',
        ),
    ]
