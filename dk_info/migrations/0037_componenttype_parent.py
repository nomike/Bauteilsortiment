# Generated by Django 4.1.7 on 2023-03-19 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dk_info', '0036_merchant_url_alter_merchant_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='componenttype',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dk_info.componenttype'),
        ),
    ]