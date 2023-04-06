# Generated by Django 3.2.16 on 2023-04-04 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(default=0)),
                ('lng', models.FloatField(default=0)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('paypal_email', models.EmailField(blank=True, max_length=255)),
                ('fcm_token', models.TextField(blank=True)),
                ('car_make', models.CharField(blank=True, max_length=255)),
                ('car_model', models.CharField(blank=True, max_length=255)),
                ('plate_number', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='courier', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='customer/avatars/')),
                ('address', models.CharField(blank=True, max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('stripe_customer_id', models.CharField(blank=True, max_length=255)),
                ('stripe_payment_method_id', models.CharField(blank=True, max_length=255)),
                ('stripe_card_last4', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('size', models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], default='medium', max_length=20)),
                ('quantity', models.IntegerField(default=1)),
                ('photo', models.ImageField(upload_to='job/photos/')),
                ('status', models.CharField(choices=[('creating', 'Creating'), ('Processing Order', 'Processing'), ('Picking Up', 'Picking'), ('Delivering Order', 'Delivering'), ('Order Completed', 'Completed'), ('Canceled', 'Canceled')], default='creating', max_length=20)),
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
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category')),
                ('courier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.courier')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_description', models.TextField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='service_images')),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500)),
                ('total', models.IntegerField()),
                ('status', models.IntegerField(choices=[(1, 'Processing'), (2, 'Ready'), (3, 'On the way'), (4, 'Delivered')])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('picked_at', models.DateTimeField(blank=True, null=True)),
                ('courier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.courier')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.customer')),
            ],
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
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='rest_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('sub_total', models.IntegerField()),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.meal')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_details', to='core.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.restaurant'),
        ),
        migrations.AddField(
            model_name='meal',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='core.restaurant'),
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('couriers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.courier')),
                ('customers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
                ('jobs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.job')),
            ],
        ),
    ]
