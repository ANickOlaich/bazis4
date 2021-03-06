# Generated by Django 3.2.11 on 2022-01-30 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bazis', '0008_alter_texture_mtexture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0)),
                ('size', models.FloatField(default=0)),
                ('length', models.FloatField(default=0)),
                ('posx', models.FloatField(default=0)),
                ('posy', models.FloatField(default=0)),
                ('posz', models.FloatField(default=0)),
                ('rotx', models.FloatField(default=0)),
                ('roty', models.FloatField(default=0)),
                ('rotz', models.FloatField(default=0)),
                ('rotw', models.FloatField(default=0)),
                ('mebel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bazis.mebel')),
            ],
        ),
    ]
