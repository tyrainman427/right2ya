# Generated by Django 3.2.16 on 2023-05-19 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20230518_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='rated',
            field=models.BooleanField(default=False),
        ),
    ]