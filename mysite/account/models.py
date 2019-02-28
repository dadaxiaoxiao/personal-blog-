from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  #外键，一对一的关联
    birth = models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=20,null=True)

    def __str__(self):
        return 'user{}'.format(self.user.username)

#个人信息数据模型
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 外键，一对一的关联
    school = models.CharField(max_length=100,blank=True)
    company = models.CharField(max_length=100,blank=True)             #公司
    profession = models.CharField(max_length=100,blank=True)          #职业
    address = models.CharField(max_length=100,blank=True)
    aboutme = models.TextField(max_length=100,blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return 'user{}'.format(self.user.username)


