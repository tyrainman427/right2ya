# Generated by Django 4.1.5 on 2023-01-29 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='method_of_payment',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Zelle', 'Zelle'), ('Cashapp', 'Cashapp'), ('Venmo', 'Venmo')], default='Cash', max_length=50),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='type_of_payment',
            field=models.CharField(choices=[('Advance Payment Deposit', 'Advance Payment Deposit'), ('Full Amount', 'Full Amount')], default='Advance Payment Deposit', max_length=50),
        ),
    ]