# Generated by Django 2.2.3 on 2019-07-29 19:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('checkout', '0003_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_option',
            field=models.CharField(
                choices=[('deposit', 'Depósito em conta'), ('pagseguro', 'Pag Seguro'), ('paypal', 'PayPal')],
                default='deposit', max_length=20, verbose_name='Opção de pagamento'),
        ),
    ]
