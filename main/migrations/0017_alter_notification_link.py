# Generated by Django 5.0 on 2024-01-14 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_notification_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='link',
            field=models.CharField(max_length=60),
        ),
    ]