# Generated by Django 3.2.16 on 2023-06-14 04:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledJob',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)),

                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(default=1)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='job/photos/')),
                ('status', models.CharField(choices=[('creating', 'Creating'), ('processing', 'Processing'), ('ready', 'Ready'), ('picking', 'Picking'), ('Delivering Order', 'Delivering'), ('completed', 'Completed'), ('reviewed', 'Reviewed'), ('canceled', 'Canceled')], default='creating', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('pickup_address', models.CharField(blank=True, max_length=255)),
                ('pickup_lat', models.FloatField(default=0)),
                ('pickup_lng', models.FloatField(default=0)),
                ('pickup_name', models.CharField(blank=True, max_length=255)),
                ('pickup_phone', models.CharField(blank=True, max_length=50)),
                ('delivery_address', models.CharField(blank=True, max_length=255)),
                ('delivery_lat', models.FloatField(default=0)),
                ('delivery_lng', models.FloatField(default=0)),
                ('delivery_name', models.CharField(blank=True, max_length=255)),
                ('delivery_phone', models.CharField(blank=True, max_length=50)),
                ('duration', models.IntegerField(default=0)),
                ('distance', models.FloatField(default=0)),
                ('price', models.FloatField(default=0)),
                ('pickup_photo', models.ImageField(blank=True, null=True, upload_to='job/pickup_photos/')),
                ('pickedup_at', models.DateTimeField(blank=True, null=True)),
                ('delivery_photo', models.ImageField(blank=True, null=True, upload_to='job/delivery_photos/')),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('delivery_date_time', models.DateField(blank=True, null=True)),
                ('delivery_time', models.TimeField(blank=True, null=True)),
                ('service_fee', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('delivery_fee', models.FloatField(default=0)),
                ('scheduled_datetime', models.DateTimeField()),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
        ),
    ]
