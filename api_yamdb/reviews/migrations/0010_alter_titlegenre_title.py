# Generated by Django 4.0.6 on 2022-07-26 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_rename_discription_title_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titlegenre',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='reviews.title'),
        ),
    ]