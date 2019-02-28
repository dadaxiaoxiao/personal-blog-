from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BlogArticles(models.Model): #注意基类
    '''
        标题，内容，作者，发布时间
    '''
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-publish",)

    def str(self):
        return self.title