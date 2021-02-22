# Generated by Django 3.0.6 on 2020-05-31 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_auto_20200531_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='drinking',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ("Doesn't matter", "Doesn't matter")], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='interested_in',
            field=models.CharField(choices=[('Men', 'Men'), ('Women', 'Women'), ('Both', 'Both')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='looking_for',
            field=models.CharField(choices=[('Serious Relationship', 'Serious Relationship'), ('Sexual Partner', 'Sexual Partner'), ('Sugar Daddy', 'Sugar Daddy'), ('Any', 'Any')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='maximum_age',
            field=models.PositiveIntegerField(default=99),
        ),
        migrations.AlterField(
            model_name='profile',
            name='minimum_age',
            field=models.PositiveIntegerField(default=18),
        ),
        migrations.AlterField(
            model_name='profile',
            name='smoking',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ("Doesn't matter", "Doesn't matter")], default='', max_length=30),
        ),
    ]
