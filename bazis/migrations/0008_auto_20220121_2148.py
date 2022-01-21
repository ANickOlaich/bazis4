# Generated by Django 3.2.11 on 2022-01-21 19:48

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bazis', '0007_auto_20220121_2143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': 'Материал', 'verbose_name_plural': 'материала'},
        ),
        migrations.AlterField(
            model_name='material',
            name='alphaMap',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None),
        ),
    ]