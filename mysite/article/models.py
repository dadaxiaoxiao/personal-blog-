from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify

class ArticleColumn(models.Model):             # 栏目
    user = models.ForeignKey(User, related_name='article_column', on_delete=models.CASCADE)
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    #字段在第一次实例是保存当前时间

    def __str__(self):
        return self.column

# 文章标签

class ArticleTag(models.Model):
    author = models.ForeignKey(User, related_name="tag",on_delete=models.CASCADE)    # 标签与作者，多对一的关系
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag


class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name="article", on_delete=models.CASCADE)  # 作者
    title = models.CharField(max_length=200)  # 标题
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, related_name="article_column", on_delete=models.CASCADE)  # 栏目
    body = models.TextField()  # 内容
    created = models.DateTimeField(default=timezone.now)  # 创造时间
    updated = models.DateTimeField(auto_now=True)  # 更新时间
    users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)
    article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True)  # 文章标签

    class Meta:
        ordering = ("-updated",)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        return reverse("article:list_article_detail", args=[self.id, self.slug])

class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, related_name="comments",on_delete=models.CASCADE)   # 一篇文章对应多个评论 多对一
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username, self.article)