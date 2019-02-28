from django.db import models
from django.contrib.auth.models import User
from slugify import slugify

class Image(models.Model):
    user = models.ForeignKey(User, related_name="images",on_delete=models.CASCADE)     # 图片的拥有者，一对多的关系
    title = models.CharField(max_length=300)                  # 图片的标题
    url = models.URLField()                                   # 存储网络图片的URL ,不规定最大长度
    slug = models.SlugField(max_length=500, blank=True)       # Image 的slug 字段
    description = models.TextField(blank=True)                # 描述图片的文本内容
    created = models.DateField(auto_now_add=True, db_index=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d')   # 上传到服务器的物理存储地址

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)    #存储

