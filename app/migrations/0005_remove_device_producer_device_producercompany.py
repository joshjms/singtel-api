# Generated by Django 4.1.5 on 2023-01-15 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_producer_alter_device_producer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='producer',
        ),
        migrations.AddField(
            model_name='device',
            name='producerCompany',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='app.producer'),
            preserve_default=False,
        ),
    ]