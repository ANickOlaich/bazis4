# Generated by Django 3.2.11 on 2022-01-29 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazis', '0003_auto_20220129_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='panels',
            name='height',
            field=models.FloatField(default=0, verbose_name='Длина'),
        ),
        migrations.AddField(
            model_name='panels',
            name='width',
            field=models.FloatField(default=0, verbose_name='Ширина'),
        ),
        migrations.AlterField(
            model_name='panels',
            name='material',
            field=models.CharField(default='', max_length=100, verbose_name='Материал Базиса'),
        ),
        migrations.AlterField(
            model_name='panels',
            name='texture',
            field=models.IntegerField(default=0, verbose_name='Направление текстуры'),
        ),
        migrations.AlterField(
            model_name='panels',
            name='thickness',
            field=models.FloatField(default=0, verbose_name='Толщина'),
        ),
    ]