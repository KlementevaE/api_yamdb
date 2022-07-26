# Generated by Django 2.2.16 on 2022-07-25 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_remove_title_genre'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='titlegenre',
            constraint=models.UniqueConstraint(fields=('title', 'genre'), name='unique_connection'),
        ),
    ]
