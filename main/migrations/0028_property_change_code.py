# Generated by Django 2.1.5 on 2019-02-02 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20190129_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='change_code',
            field=models.CharField(default=None, max_length=4),
        ),
    ]