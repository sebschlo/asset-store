from django.contrib import admin
from django import forms
from .models import *

# Register your models here.
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    class AssetDetailInline(admin.TabularInline):
        model = AssetDetail
        extra = 1
        formfield_overrides = {
            models.TextField: {'widget': forms.Textarea(attrs={'rows': 1, 'cols': 50})},
        }

    inlines = (AssetDetailInline, )
    list_display = ('name', 'asset_type', 'asset_class')
    list_filter = ('asset_type', 'asset_class')
    search_fields = ('name',)