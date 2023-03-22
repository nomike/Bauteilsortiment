# Generated by Django 4.1.7 on 2023-03-19 01:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dk_info', '0014_alter_digikeycomponent_cache_expiry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]