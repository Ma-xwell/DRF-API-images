# Generated by Django 4.1.6 on 2023-03-07 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images_api', '0010_alter_image_is_expirable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='is_expirable',
            field=models.BooleanField(),
        ),
    ]
