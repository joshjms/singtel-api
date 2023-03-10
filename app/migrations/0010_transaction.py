# Generated by Django 4.1.5 on 2023-01-16 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_device_producer_alter_sale_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactionType', models.CharField(max_length=10)),
                ('transactionDate', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='app.device')),
            ],
        ),
    ]
