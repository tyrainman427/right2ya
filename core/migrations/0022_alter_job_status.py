# Generated by Django 3.2.16 on 2023-10-07 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_job_is_scheduled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('creating', 'Creating'), ('processing', 'Processing'), ('ready', 'Ready'), ('picking', 'Picking'), ('arrived', 'Arrived'), ('delivering', 'Delivering'), ('signed', 'Signed'), ('completed', 'Completed'), ('reviewed', 'Reviewed'), ('canceled', 'Canceled'), ('scheduled', 'Scheduled')], default='creating', max_length=20),
        ),
    ]