# Generated by Django 3.2.16 on 2023-10-17 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20231017_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='tipped',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_tipped', to='core.tip'),
        ),
    ]
