# Generated by Django 2.1.5 on 2019-02-10 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_property_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='mottoemailphone',
            name='facebook',
            field=models.URLField(default='http://facebook.com'),
        ),
        migrations.AddField(
            model_name='mottoemailphone',
            name='linkedin',
            field=models.URLField(default='http://linkedin.com'),
        ),
    ]
