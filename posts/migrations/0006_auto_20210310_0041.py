# Generated by Django 2.2.9 on 2021-03-09 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20210228_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
