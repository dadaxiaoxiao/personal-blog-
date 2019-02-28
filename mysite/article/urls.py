from django.urls import path,re_path
from . import views,list_views


urlpatterns = [
    path('article-column/', views.article_column, name='article_column'),  # 栏目管理
    path('rename-column/', views.rename_article_column, name='rename_article_column'),    # 修改栏目
    path('del-column/', views.del_article_column, name="del_article_column"),          # 删除栏目
    path('article-post/', views.article_post, name='article_post'),                     # 发表文章
    path('article-list/',views.article_list,name='article_list'),                       # 文章标题列表
    re_path('article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/',views.article_detail,name='article_detail'),   # 反定向 标题对应的文章
    path('del-article/',views.del_article,name='del_article'),                           # 删除
    re_path('redit-article/(?P<article_id>\d+)/', views.redit_article, name='redit_article'),     # 修改


    path('list-article-titles/',list_views.article_titles,name='article_titles'),                    # 列表

    re_path('list--article--detail/(?P<id>\d+)/(?P<slug>[-\w]+)/', list_views.article_detail, name="list_article_detail"),
    re_path('list-article-titles/(?P<username>[-\w]+)/', list_views.article_titles, name="author_articles"),            # 指定作者文章列表
    path('like-article/', list_views.like_article, name="like_article"),                               # 点赞
    path('rticle-tag/', views.article_tag, name="article_tag"),                                        # 增加标签
    path('del-article-tag/', views.del_article_tag, name="del_article_tag"),                           # 删除标签

]
app_name = 'article'
