# Generated by Django 3.2.11 on 2022-01-30 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazis', '0007_alter_panels_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='texture',
            name='mtexture',
            field=models.ImageField(default='default.jpg', upload_to='texture'),
        ),
    ]
