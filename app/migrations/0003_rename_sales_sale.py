# Generated by Django 4.1.5 on 2023-01-15 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_week_weekid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sales',
            new_name='Sale',
        ),
    ]
