# Generated by Django 4.2.16 on 2024-11-30 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_transaction_transaction_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='link',
        ),
    ]
