# Generated by Django 3.1.2 on 2021-04-13 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webnavigate', '0002_auto_20210412_2305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='website',
            old_name='address',
            new_name='site_address',
        ),
        migrations.RenameField(
            model_name='website',
            old_name='entity',
            new_name='site_name',
        ),
    ]
