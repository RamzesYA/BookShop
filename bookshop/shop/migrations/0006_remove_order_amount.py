# Generated by Django 5.1.2 on 2024-10-27 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_shoppingcart_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='amount',
        ),
    ]
