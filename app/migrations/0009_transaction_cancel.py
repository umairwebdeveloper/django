# Generated by Django 4.2.16 on 2024-12-03 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='cancel',
            field=models.BooleanField(default=False),
        ),
    ]
