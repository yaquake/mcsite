# Generated by Django 2.1.3 on 2019-01-05 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20190105_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='thumbnail',
            field=models.ImageField(default=None, null=True, upload_to='property_images/'),
        ),
    ]
