# Generated by Django 3.0.6 on 2020-08-04 18:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_auto_20200727_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversationmessage',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
