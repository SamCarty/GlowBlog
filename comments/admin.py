from django.contrib import admin

from comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_date')
    list_display_links = ('content',)
    list_filter = ('author', 'created_date')
    search_fields = ('content',)
    list_per_page = 10


admin.site.register(Comment, CommentAdmin)
