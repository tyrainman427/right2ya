# Generated by Django 4.1.4 on 2023-01-08 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newContract', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='total_price',
            field=models.IntegerField(null=True),
        ),
    ]
