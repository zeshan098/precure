# Generated by Django 3.2.9 on 2021-12-08 12:09

import django.contrib.postgres.fields
from django.db import migrations, models
import multi_email_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211208_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffuser',
            name='buyer_model',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='staffuser',
            name='category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='staffuser',
            name='emails',
            field=multi_email_field.fields.MultiEmailField(default=[]),
        ),
        migrations.AddField(
            model_name='staffuser',
            name='menufacture',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
    ]
