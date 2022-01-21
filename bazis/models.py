from tkinter import CASCADE
from django.conf import settings
from colorfield.fields import ColorField
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# Текстуры
class Texture(models.Model):
    title = models.CharField('Название',max_length=50, default='default.jpg')
    mtexture = models.ImageField(upload_to ='bazis/static/texture/', default='default.jpg')
    @property
    def thumbnail_preview(self):
        if self.mtexture:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.mtexture.url))
        return ""
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Текстуру'
        verbose_name_plural = 'Текстуры'
        


# Типы материалов
class MaterialType(models.Model):
    title = models.CharField(max_length=50 , default='ЛДСП')
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Тип материала'
        verbose_name_plural = 'Типы материалов'

# Материал для three.js
class Material(models.Model):
    title = models.CharField('Название',max_length=100)
    alphaMap = ColorField('Непрозрачность',default='#FFFFFF')
    color = ColorField('Цвет',default='#999999')
    metalness = models.FloatField('Метал',default=0.5)
    roughness = models.FloatField('Шероховатость',default=0.5) #Шерохотатость 0-зеркало 1- полностью рассеяный
    map = models.ForeignKey(Texture, on_delete = models.CASCADE) # Текстура
    type = models.ForeignKey(MaterialType, on_delete = models.CASCADE) # Тип Материала 
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'