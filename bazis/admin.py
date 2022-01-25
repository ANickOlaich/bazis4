from ast import Return
from turtle import title
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Material, MaterialType, Post, Texture, file_import, Mebel, Panels, Contours, MaterialEqual
import json




class TextureAdmin(admin.ModelAdmin):

    list_display = ( 'title', 'thumbnail_preview')
    readonly_fields = ('thumbnail_preview',)
    search_fields = ('title', )
    
    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Предпросмотр'
    thumbnail_preview.allow_tags = True
    
    def button(self, obj):
        return mark_safe(f'<a class="button" >Кнопка</a>')



class PostMaterial(admin.ModelAdmin):
    list_display = ('title', 'type')
    search_fields = ('title', )
    



    
class MebelAdmin(admin.ModelAdmin):
   change_list_template = 'admin/bazis/mebel/change_list.html' 
   
class ImportAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        
        with open(obj.file.path, "r") as read_file:
            data = json.load(read_file)
            NewMebel = Mebel(title = 'Импорт' , width = data['Width'], height = data['Height'], depth = data['Depth'])
            NewMebel.save()
            NewPanels = data['Panels']
            for panel in NewPanels:
                NewPanel = Panels(  title       = panel['Name'],
                                    thickness   = panel['Thickness'], 
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
                                          #arc_dir       = cont['ArcDir']
                                          )
                    NewContour.save()
        allMaterials = Panels.objects.filter(mebel=NewMebel).values('material').distinct()
        for mat in allMaterials:
            NewMaterialEq=MaterialEqual(materialName=mat['material'],mebel=NewMebel)
            NewMaterialEq.save()
            
             
#ProductOrder.objects.values('Category').distinct()







admin.site.register(Post)
admin.site.register(Texture, TextureAdmin) 
admin.site.register(MaterialType)
admin.site.register(Material, PostMaterial)
admin.site.register(Mebel,MebelAdmin)
admin.site.register(file_import, ImportAdmin)
admin.site.register(MaterialEqual)
admin.site.register(Panels)





