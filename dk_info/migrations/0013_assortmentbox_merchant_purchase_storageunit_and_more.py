# Generated by Django 4.1.7 on 2023-03-19 01:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dk_info', '0012_alter_component_detailed_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssortmentBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2023, 3, 19, 1, 58, 16, 723304, tzinfo=datetime.timezone.utc))),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dk_info.merchant')),
            ],
        ),
        migrations.CreateModel(
            name='StorageUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('assortment_box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dk_info.assortmentbox')),
            ],
        ),
        migrations.CreateModel(
            name='StorageUnitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('width', models.IntegerField(null=True)),
                ('height', models.IntegerField(null=True)),
                ('depth', models.IntegerField(null=True)),
                ('template', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='component',
            name='cache_expiry',
        ),
        migrations.CreateModel(
            name='DigiKeyComponent',
            fields=[
                ('component_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dk_info.component')),
                ('cache_expiry', models.DateTimeField(default=datetime.datetime(2023, 3, 19, 1, 58, 16, 721190, tzinfo=datetime.timezone.utc))),
            ],
            bases=('dk_info.component',),
        ),
        migrations.CreateModel(
            name='StorageUnitCompartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('storage_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dk_info.storageunit')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dk_info.component')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dk_info.purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2023, 3, 19, 1, 58, 16, 722047, tzinfo=datetime.timezone.utc))),
                ('count', models.IntegerField()),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dk_info.component')),
            ],
        ),
        migrations.AddField(
            model_name='component',
            name='storage_unit_compartment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dk_info.storageunitcompartment'),
        ),
    ]