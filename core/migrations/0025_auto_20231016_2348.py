# Generated by Django 3.2.16 on 2023-10-17 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20231008_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='stripe_payment_intent_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('creating', 'Creating'), ('processing', 'Processing Order'), ('ready', 'Ready for Driver'), ('picking', 'Picking Up Order'), ('arrived', 'Arrived'), ('delivering', 'Delivering Order'), ('signed', 'Order Signed'), ('completed', 'Completed'), ('reviewed', 'Reviewed'), ('canceled', 'Canceled'), ('scheduled', 'Scheduled')], default='creating', max_length=20),
        ),
    ]