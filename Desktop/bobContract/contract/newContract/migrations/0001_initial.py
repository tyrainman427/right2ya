# Generated by Django 4.1.4 on 2023-01-08 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('add_photos', models.BooleanField(default=False)),
                ('add_lights', models.BooleanField(default=False)),
                ('add_more_time', models.BooleanField(default=False)),
                ('type_of_payment', models.CharField(max_length=50)),
                ('method_of_payment', models.CharField(max_length=50)),
                ('total_price', models.IntegerField()),
            ],
        ),
    ]
