# Generated by Django 3.2.16 on 2023-07-30 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='text',
        ),
    ]