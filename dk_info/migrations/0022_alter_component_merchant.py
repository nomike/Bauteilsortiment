# Generated by Django 4.1.7 on 2023-03-19 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dk_info', '0021_component_merchant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dk_info.merchant'),
        ),
    ]