# Generated by Django 4.2.11 on 2024-07-06 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_menu_discount_menu_percent_discount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='int_discount',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='percent_discount',
        ),
        migrations.AlterField(
            model_name='menu',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='скидка в $'),
        ),
    ]
