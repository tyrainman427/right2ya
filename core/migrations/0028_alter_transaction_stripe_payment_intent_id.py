# Generated by Django 3.2.16 on 2023-10-20 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_job_tipped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='stripe_payment_intent_id',
            field=models.CharField(max_length=255),
        ),
    ]
