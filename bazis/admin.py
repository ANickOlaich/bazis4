from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Material, MaterialType, Post, Texture

class PostAdmin(admin.ModelAdmin):

    list_display = ( 'title', 'thumbnail_preview')
    readonly_fields = ('thumbnail_preview',)
    search_fields = ('title', )
    
    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Предпросмотр'
    thumbnail_preview.allow_tags = True

class PostMaterial(admin.ModelAdmin):
    list_display = ('title', 'type')
    search_fields = ('title', )

admin.site.register(Post)
admin.site.register(Texture, PostAdmin) 
admin.site.register(MaterialType)
admin.site.register(Material, PostMaterial)