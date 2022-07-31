# Generated by Django 2.2.16 on 2022-07-26 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20220726_1925'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='confirmationcode',
            name='unique_username_code',
        ),
        migrations.AddConstraint(
            model_name='confirmationcode',
            constraint=models.UniqueConstraint(fields=('username', 'confirmation_code'), name='unique_username_code'),
        ),
    ]
