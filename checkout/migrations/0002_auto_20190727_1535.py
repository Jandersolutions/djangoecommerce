# Generated by Django 2.2.3 on 2019-07-27 18:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('catalogo', '__first__'),
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart_key', 'product')},
        ),
    ]
