# Generated by Django 4.1.7 on 2023-04-03 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0004_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boxes.customuser'),
        ),
    ]
