# Generated by Django 4.1.5 on 2023-01-26 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='menu_images/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('category', models.ManyToManyField(related_name='item', to='customer.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('client_full_name', models.CharField(max_length=75)),
                ('contact_person', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=75)),
                ('state', models.CharField(max_length=2)),
                ('zip_code', models.CharField(max_length=5)),
                ('telephone_number', models.CharField(max_length=10)),
                ('cell_number', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('date_of_event', models.CharField(max_length=50)),
                ('event_type', models.CharField(max_length=50)),
                ('number_of_guests', models.CharField(max_length=3)),
                ('start_time', models.CharField(max_length=50)),
                ('end_time', models.CharField(max_length=50)),
                ('location_of_event', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=10)),
                ('type_of_payment', models.CharField(max_length=50)),
                ('method_of_payment', models.CharField(max_length=50)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(blank=True, related_name='order', to='customer.menuitem')),
            ],
        ),
    ]