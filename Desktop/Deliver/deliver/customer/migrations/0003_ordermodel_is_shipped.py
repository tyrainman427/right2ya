# Generated by Django 4.1.5 on 2023-01-24 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_ordermodel_street'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]
