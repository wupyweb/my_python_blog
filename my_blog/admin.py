from django.contrib import admin
from .models import Article, Comment, Category
from django.db import models

from mdeditor.widgets import MDEditorWidget

# Register your models here.
# admin.site.register(Article)


@admin.register(Article)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status',)
    list_filter = ('status', 'created', 'publish', 'author',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish',)

    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


admin.site.register(Comment)
admin.site.register(Category)
