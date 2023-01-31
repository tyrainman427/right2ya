# Generated by Django 3.2.16 on 2023-01-30 01:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_auto_20230129_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='delivery_photo',
            field=models.ImageField(blank=True, null=True, upload_to='job/delivery_photos/'),
        ),
        migrations.AddField(
            model_name='job',
            name='distance',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='job',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='job',
            name='pickedup_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='pickup_photo',
            field=models.ImageField(blank=True, null=True, upload_to='job/pickup_photos/'),
        ),
        migrations.AddField(
            model_name='job',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='job',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category'),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('creating', 'Creating'), ('processing', 'Processing'), ('picking', 'Picking'), ('delivering', 'Delivering'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='creating', max_length=20),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_payment_intent_id', models.CharField(max_length=255, unique=True)),
                ('amount', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('in', 'In'), ('out', 'Out')], default='in', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.job')),
            ],
        ),
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(default=0)),
                ('lng', models.FloatField(default=0)),
                ('paypal_email', models.EmailField(blank=True, max_length=255)),
                ('fcm_token', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.courier'),
        ),
    ]
