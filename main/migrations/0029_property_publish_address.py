# Generated by Django 2.1.5 on 2019-02-02 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_property_change_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='publish_address',
            field=models.IntegerField(default=0, max_length=3),
        ),
    ]