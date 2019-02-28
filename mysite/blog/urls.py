from django.urls import path,re_path

from . import views
urlpatterns = [
    # home
    path('', views.blog_title, name='blog_title'),
    re_path('(?P<article_id>\d+)/', views.blog_article, name='blog_detail'), #detail 详细的意思

]
app_name = 'blog'