# Generated by Django 5.2.1 on 2025-05-19 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_alert_networktraffic_resourceusage_server_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='server_id',
            new_name='server',
        ),
        migrations.AlterField(
            model_name='server',
            name='ip_address',
            field=models.CharField(max_length=20),
        ),
    ]
