# Generated by Django 2.0.7 on 2018-07-06 03:04

from django.db import migrations, models
import pyotp


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pass_key',
            field=models.CharField(default=pyotp.random_base32, editable=False, max_length=25),
        ),
    ]
