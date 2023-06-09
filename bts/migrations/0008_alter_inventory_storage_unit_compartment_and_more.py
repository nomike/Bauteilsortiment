# Generated by Django 4.1.7 on 2023-04-09 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bts', '0007_remove_inventory_component_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='storage_unit_compartment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventories', to='bts.storageunitcompartment'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='url',
            field=models.URLField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='storageunitcompartment',
            name='storage_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storage_unit_compartments', to='bts.storageunit'),
        ),
        migrations.AlterUniqueTogether(
            name='component',
            unique_together={('part_number', 'merchant')},
        ),
    ]
