# Generated by Django 3.2.16 on 2023-05-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating_value',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]