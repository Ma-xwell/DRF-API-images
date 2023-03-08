from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AccountTier, ImageDimensions, Image


class ImageDimensionsInline(admin.TabularInline):
    model = ImageDimensions
    extra = 1
    
class AccountTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'generate_expiring_links', 'original_file_link_presence', 'description')
    search_fields = ['name']
    inlines = [ImageDimensionsInline]

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'tier_type')
    UserAdmin.fieldsets += (
        ('Tier', {'fields': ('tier_type',)}),
    )
    

admin.site.register(User, CustomUserAdmin)
admin.site.register(AccountTier, AccountTierAdmin)
admin.site.register(ImageDimensions)
admin.site.register(Image)