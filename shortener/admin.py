from django.contrib import admin
from .models import FullURL, Shortcut


@admin.register(Shortcut)
class ShortcutAdmin(admin.ModelAdmin):
    list_display = ('value', 'full_url')

class ShortcutInline(admin.TabularInline):
    model = Shortcut

@admin.register(FullURL)
class LinkAdmin(admin.ModelAdmin):
    inlines = (ShortcutInline,)
