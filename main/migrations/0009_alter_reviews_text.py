# Generated by Django 4.2.11 on 2024-07-11 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_reviews_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='text',
            field=models.CharField(help_text='напишите отзыв здесь', max_length=250, verbose_name='отзыв'),
        ),
    ]
