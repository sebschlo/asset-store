from django.contrib import admin
from django import forms
from .models import *

# Register your models here.
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    class AssetDetailInline(admin.TabularInline):
        model = AssetDetail
        extra = 1
        # Make text field reasonably sized
        formfield_overrides = {
            models.TextField: {'widget': forms.Textarea(attrs={'rows': 1, 'cols': 50})},
        }

    # Add inline asset details
    inlines = (AssetDetailInline, )
    # Show relevant columns on the list view
    list_display = ('name', 'asset_type', 'asset_class')
    # Add filtering capabilities
    list_filter = ('asset_type', 'asset_class')
    # Add a search bar
    search_fields = ('name',)