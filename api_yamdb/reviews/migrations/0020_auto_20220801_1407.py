# Generated by Django 2.2.19 on 2022-08-01 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0019_auto_20220801_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-pk'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug категории'),
        ),
    ]
