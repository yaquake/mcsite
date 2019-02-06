# Generated by Django 2.1.5 on 2019-02-05 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_auto_20190204_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_host', models.CharField(max_length=40)),
                ('email_port', models.PositiveIntegerField()),
                ('email_host_user', models.CharField(max_length=50)),
                ('email_host_password', models.CharField(max_length=50)),
                ('email_use_ssl', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Email settings',
                'verbose_name_plural': 'Email settings',
            },
        ),
    ]