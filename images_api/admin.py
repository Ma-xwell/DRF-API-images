from django.contrib import admin
from .models import User, AccountTier, ImageDimensions, Image


# Register your models here.

class ImageDimensionsInline(admin.TabularInline):
    model = ImageDimensions
    extra = 1
    
class AccountTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'generate_expiring_links', 'original_file_link_presence', 'description')
    search_fields = ['name']
    inlines = [ImageDimensionsInline]

admin.site.register(User)
admin.site.register(AccountTier, AccountTierAdmin)
admin.site.register(ImageDimensions)
admin.site.register(Image)