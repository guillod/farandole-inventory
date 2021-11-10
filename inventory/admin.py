from django.contrib import admin
from django.utils.html import format_html

from .models import Object, Group, Location, State

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('description','nb','group','location','state','photo_thumbnail','supplier','price', 'buy_at','created_at','updated_at')
    list_filter = ['group','location','state', 'created_by','updated_by']
    search_fields = ['description']
    fields = [('description','nb'),('group','location','state'),('photo_display','photo'),('supplier','price', 'buy_at'),'comment',('created_at','created_by','updated_at','updated_by')]
    readonly_fields = ['photo_display','created_at','created_by','updated_at','updated_by']
    save_as = True

    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html('<a href="{0}"><img src="{0}" style="max-height:50px;max-width:100px;" /></a>', obj.photo.url)
    photo_thumbnail.__name__ = "Photo"
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by_id = request.user.id
        obj.updated_by_id = request.user.id
        obj.save()

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group',)

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('state',)
