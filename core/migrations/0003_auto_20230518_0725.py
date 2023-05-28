# Generated by Django 3.2.16 on 2023-05-18 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_customer_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='company',
        ),
        migrations.AddField(
            model_name='courier',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]