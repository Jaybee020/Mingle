# Generated by Django 3.0.6 on 2020-07-21 16:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20200721_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversations',
            name='last_contact',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
