# Generated by Django 4.1.7 on 2023-04-03 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0009_alter_box_area_alter_box_volume'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
