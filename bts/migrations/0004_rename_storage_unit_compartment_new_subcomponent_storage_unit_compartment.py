# Generated by Django 4.1.7 on 2023-03-23 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bts', '0003_remove_subcomponent_storage_unit_compartment_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcomponent',
            old_name='storage_unit_compartment_new',
            new_name='storage_unit_compartment',
        ),
    ]
