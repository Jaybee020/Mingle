# Generated by Django 3.0.6 on 2020-08-11 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_auto_20200804_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationmessage',
            name='vocie_record',
            field=models.FileField(blank=True, upload_to='voice record'),
        ),
    ]
