# Generated by Django 4.2.11 on 2024-06-02 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_temporary_avatar_temp_avatar'),
    ]

    operations = [
        migrations.DeleteModel(
            name='temporary_avatar',
        ),
    ]