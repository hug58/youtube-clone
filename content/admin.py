from django.contrib import admin
from .models import Comment,  Video

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at', 'content_object')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'created_at', 'updated_at', 'likes_count_display', 'dislikes_count_display')
    list_filter = ('created_at', 'uploader')
    search_fields = ('title', 'uploader__username')
    readonly_fields = ('likes_count_display',)


