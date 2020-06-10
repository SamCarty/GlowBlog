from django.contrib import admin

from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'last_modified_date')
    list_display_links = ('title',)
    list_filter = ('author', 'created_date')
    search_fields = ('title', 'content')
    list_per_page = 10


admin.site.register(Article, ArticleAdmin)
