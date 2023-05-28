# Generated by Django 3.2.16 on 2023-05-18 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20230518_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('review_text', models.TextField()),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.courier')),
            ],
        ),
    ]