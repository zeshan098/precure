# Generated by Django 3.2.9 on 2021-12-24 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0007_rename_buyermodels_vendormodels'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorPO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_no', models.CharField(blank=True, max_length=200, null=True)),
                ('quotation', models.TextField(blank=True, null=True)),
                ('sub_total', models.CharField(blank=True, max_length=200, null=True)),
                ('discount', models.CharField(blank=True, max_length=200, null=True)),
                ('total_amount', models.CharField(blank=True, max_length=200, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('attachment_file', models.FileField(blank=True, null=True, upload_to='')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('update_datetime', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, choices=[('1', 'Send'), ('2', 'Close')], max_length=20, null=True)),
            ],
        ),
    ]
