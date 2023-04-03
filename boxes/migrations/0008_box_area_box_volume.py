# Generated by Django 4.1.7 on 2023-04-03 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0007_alter_box_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='area',
            field=models.DecimalField(decimal_places=2, default='1.00', max_digits=10),
        ),
        migrations.AddField(
            model_name='box',
            name='volume',
            field=models.DecimalField(decimal_places=2, default='1.00', max_digits=10),
        ),
    ]
