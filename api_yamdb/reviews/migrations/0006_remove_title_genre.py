# Generated by Django 2.2.16 on 2022-07-25 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220725_0345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
    ]
