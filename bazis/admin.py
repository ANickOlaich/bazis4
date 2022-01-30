from ast import Return
from turtle import pos, title, width
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Material, MaterialType, Post, Texture, file_import, Mebel, Panels, Contours, MaterialEqual, Size
import json




class TextureAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'thumbnail_preview')
    readonly_fields = ('title','thumbnail_preview',)
    search_fields = ('title', )
    
    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview
    
    def save_model(self, request, obj, form, change):
        obj.title=obj.mtexture.name
        super().save_model(request, obj, form, change)
        print(obj.mtexture.name)

    thumbnail_preview.short_description = 'Предпросмотр'
    thumbnail_preview.allow_tags = True
    



class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')
    search_fields = ('title', )
    change_form_template = 'admin/material_change_form.html'


class PanelInline(admin.TabularInline):
    model=Panels
    can_delete=False    #нельзя удалять
    max_num=0           #нельзя добавлять
    fields = ('pos','material', 'materialId','height','width', 'texture')
    readonly_fields = ('pos','title','material', 'height','width')
    classes = ['collapse']
    
class MaterialEqualInline(admin.TabularInline):
    model = MaterialEqual
    can_delete=False    #нельзя удалять
    max_num=0           #нельзя добавлять
    
    
class MebelAdmin(admin.ModelAdmin):
   change_list_template = 'admin/bazis/mebel/change_list.html' 
   change_form_template = 'admin/mebel_change_form.html'
   inlines = [       
        MaterialEqualInline,
        PanelInline,
   ]
   
   def save_model(self, request, obj, form, change):
       super().save_model(request, obj, form, change)    
       rs=Panels.objects.filter(mebel=obj)  
       Eqs=MaterialEqual.objects.filter(mebel=obj)      #Получаю элементы для замены
       for eq in Eqs:                                   #Перебираю элементы           
           rsm=rs.filter(material=eq.materialName)    
           for r in rsm:
               Zamena=Panels.objects.get(id=r.id)        
               Zamena.materialId=eq.materialId
               Zamena.save()
                                       
           
               
               
               
               
       #return super().save_model(request, obj, form, change)


   
class ImportAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        
        with open(obj.file.path, "r") as read_file:
            data = json.load(read_file)
            NewMebel = Mebel(title = 'Импорт' , width = data['Width'], height = data['Height'], depth = data['Depth'])
            NewMebel.save()
            NewSizes = data['Size']
            for size in NewSizes:
                NewSize = Size(
                                    value       = size['Value'],
                                    size        = size['Size'],
                                    length      = size['Length'],
                                    posx        = size['PosX'],
                                    posy        = size['PosY'],
                                    posz        = size['PosZ'],
                                    rotx        = size['RotX'],
                                    roty        = size['RotY'],
                                    rotz        = size['RotZ'],
                                    rotw        = size['RotW'],
                                    mebel       = NewMebel)
                NewSize.save()
            NewPanels = data['Panels']
            for panel in NewPanels:
                try:
                    pos = panel['Pos']
                except:
                    pos = 0
                NewPanel = Panels(  title       = panel['Name'],
                                    pos         = pos,
                                    thickness   = panel['Thickness'],
                                    width       = round(panel['Width'],1),
                                    height      = round(panel['Height'],1), 
                                    material    = panel['Material'],
                                    posx        = panel['PosX'],
                                    posy        = panel['PosY'],
                                    posz        = panel['PosZ'],
                                    rotx        = panel['RotX'],
                                    roty        = panel['RotY'],
                                    rotz        = panel['RotZ'],
                                    rotw        = panel['RotW'],
                                    texture     = panel['Texture'], 
                                    mebel       = NewMebel) 
                NewPanel.save()
                NewContours = panel['Cont']
                for cont in NewContours:
                    NewContour = Contours(type          = cont['Type'],
                                          panel         = NewPanel,
                                          pos1x         = cont['Pos1x'],
                                          pos2x         = cont['Pos2x'],
                                          pos1y         = cont['Pos1y'],
                                          pos2y         = cont['Pos2y'],
                                          centerx       = cont['CenterX'],
                                          centery       = cont['CenterY'],
                                          radius        = cont['Radius'],
                                          start_angle   = cont['StartAngle'],
                                          end_angle     = cont['EndAngle'],
                                          arc_dir       = cont['ArcDir']
                                          )
                    NewContour.save()
        allMaterials = Panels.objects.filter(mebel=NewMebel).values('material').distinct()
        for mat in allMaterials:
            NewMaterialEq=MaterialEqual(materialName=mat['material'],mebel=NewMebel)
            NewMaterialEq.save()
            
             
#ProductOrder.objects.values('Category').distinct()







admin.site.register(Post)
admin.site.register(Texture,TextureAdmin) 
admin.site.register(MaterialType)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Mebel,MebelAdmin)
admin.site.register(file_import, ImportAdmin)
admin.site.register(MaterialEqual)
admin.site.register(Panels)





