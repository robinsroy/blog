from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created', 'updated')
    list_filter = ('status', 'created', 'updated', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    ordering = ('-created',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('content', 'author__username')
    date_hierarchy = 'created'
    ordering = ('-created',)
