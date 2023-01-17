# Generated by Django 4.1.5 on 2023-01-16 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_campaign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='app.device'),
        ),
    ]