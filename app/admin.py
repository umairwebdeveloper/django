# admin.py
from django.contrib import admin
from .models import UserProfile
from django.utils.html import format_html

class ImageAdmin(admin.ModelAdmin):
    def profile_image_tag(self, obj):
        if obj.profile_image and obj.profile_image.url:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.profile_image.url))
        return "No Image"

    def id_card_front_tag(self, obj):
        if obj.id_card_front and obj.id_card_front.url:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.id_card_front.url))
        return "No Image"
    
    def id_card_back_tag(self, obj):
        if obj.id_card_back and obj.id_card_back.url:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.id_card_back.url))
        return "No Image"
    
    profile_image_tag.short_description = 'Pofile Image'
    id_card_front_tag.short_description = 'ID Card Front'
    id_card_back_tag.short_description = 'ID Card Back'
    list_display = ['user', 'status', 'created_at', 'profile_image_tag', 'id_card_front_tag', 'id_card_back_tag']
    list_editable = ['status']
    readonly_fields = ['profile_image_tag', 'id_card_front_tag', 'id_card_back_tag']

admin.site.register(UserProfile, ImageAdmin)


admin.site.site_header = "Keysavvy Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Keysavvy Admin Dashboard"