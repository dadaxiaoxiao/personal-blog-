from django.contrib import admin
from .models import BlogArticles
class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ("title","author","publish")
    list_filter = ("publish", "author")
    search_fields = ('title','body')
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ['publish','author']


#注册到admin 中
admin.site.register(BlogArticles,BlogArticlesAdmin)
