# Generated by Django 4.1.7 on 2023-03-19 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dk_info', '0032_component_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
    ]