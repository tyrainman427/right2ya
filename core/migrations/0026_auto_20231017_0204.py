# Generated by Django 3.2.16 on 2023-10-17 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20231016_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='tip',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('job', 'Job'), ('tip', 'Tip')], default='job', max_length=5),
        ),
    ]