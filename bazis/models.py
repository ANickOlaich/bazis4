from tkinter import CASCADE
from django.conf import settings
from django.forms import CharField
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
    title = models.CharField('Название',max_length=1000, default='default.jpg')
    mtexture = models.ImageField(upload_to ='texture', default='default.jpg')
    @property
    def thumbnail_preview(self):
        if self.mtexture:
            return mark_safe('<img src="{}" width="200" height="200" />'.format(self.mtexture.url))
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
    title = models.CharField('Название',max_length=1000)
    metalness = models.FloatField('Метал',default=0.5)
    roughness = models.FloatField('Шероховатость',default=0.5) #Шерохотатость 0-зеркало 1- полностью рассеяный
    map = models.ForeignKey(Texture, on_delete = models.CASCADE) # Текстура
    type = models.ForeignKey(MaterialType, on_delete = models.CASCADE) # Тип Материала 
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


    


#Модель мебели
class Mebel(models.Model):
    title = models.CharField('Название',max_length=100)   
    text = models.TextField('Описание')
    created_date = models.DateTimeField(default=timezone.now)
    width = models.FloatField('Ширина',default = 0)
    height = models.FloatField('Вісота',default = 0)
    depth = models.FloatField('Глубина',default = 0)
    visible = models.BooleanField('Видимая',default = False)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

#Модель соответствия материалов
class MaterialEqual(models.Model):
    mebel = models.ForeignKey(Mebel,on_delete = models.CASCADE, default=1)
    materialName = models.CharField('Материал',max_length=1000, default='')  
    materialId = models.ForeignKey(Material,on_delete = models.CASCADE, default=1)
    
    
    def __str__(self):
        return self.materialName
    
    class Meta:
        verbose_name = 'Материал панели'
        verbose_name_plural = 'Материал панелей'

# Модель размеров
class Size(models.Model):
    value = models.FloatField(default=0)
    size = models.FloatField(default=0)
    length = models.FloatField(default=0)
    posx = models.FloatField(default=0)
    posy = models.FloatField(default=0)
    posz = models.FloatField(default=0)
    rotx = models.FloatField(default=0)
    roty = models.FloatField(default=0)
    rotz = models.FloatField(default=0)
    rotw = models.FloatField(default=0)
    mebel = models.ForeignKey(Mebel, on_delete = models.CASCADE, null=True)
    
        
# Модель панелей
class Panels(models.Model):
    pos = models.IntegerField('Номер',default=0)
    title = models.CharField('Название',max_length=100) 
    material = models.CharField('Материал Базиса',max_length=1000, default='') 
    materialId = models.ForeignKey(Material, on_delete=models.CASCADE, default=1)
    mebel = models.ForeignKey(Mebel, on_delete = models.CASCADE, null=True)
    thickness = models.FloatField('Толщина',default=0)
    width = models.FloatField('Ширина',default=0)
    height = models.FloatField('Длина',default=0)
    posx = models.FloatField(default=0)
    posy = models.FloatField(default=0)
    posz = models.FloatField(default=0)
    rotx = models.FloatField(default=0)
    roty = models.FloatField(default=0)
    rotz = models.FloatField(default=0)
    rotw = models.FloatField(default=0)
    texture = models.IntegerField('Направление текстуры',default=0)
     
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Панель'
        verbose_name_plural = 'Панели' 

    
class Contours(models.Model):
    type = models.IntegerField(default=1)
    panel = models.ForeignKey(Panels, on_delete = models.CASCADE, default=1)
    pos1x = models.FloatField(default=0)
    pos2x = models.FloatField(default=0)
    pos1y = models.FloatField(default=0)
    pos2y = models.FloatField(default=0)
    centerx = models.FloatField(default=0)
    centery = models.FloatField(default=0)
    radius = models.FloatField(default=0)
    start_angle = models.FloatField(default=0)
    end_angle = models.FloatField(default=0)
    arc_dir = models.BooleanField(default = False)
    
    
    
    class Meta:
        verbose_name = 'Контур'
        verbose_name_plural = 'Контурі' 
    
    
#Файлы импорта
class file_import(models.Model):
    file = models.FileField('Файл',upload_to ='files_import')
    
    
    class Meta:
        verbose_name = 'Файл импорта'
        verbose_name_plural = 'Файлы импорта'
    
        


    