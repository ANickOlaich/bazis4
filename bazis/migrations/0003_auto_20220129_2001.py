# Generated by Django 3.2.11 on 2022-01-29 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazis', '0002_textures'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Textures',
        ),
        migrations.AlterField(
            model_name='texture',
            name='mtexture',
            field=models.ImageField(default='default.jpg', upload_to='texture/'),
        ),
    ]