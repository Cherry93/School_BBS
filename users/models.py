from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# user 包括 学号，姓名，专业，QQ


class User(AbstractUser):
    SEX_CHOICES = (
        ('男', 1),
        ('女', 0),)
    student_num = models.CharField(max_length=64,verbose_name="学号")
    qq_num = models.CharField(max_length=64,blank=True,verbose_name="qq号")
    major = models.CharField(max_length=64,blank=True,verbose_name="专业")
    sex = models.CharField(max_length=1,choices=SEX_CHOICES,verbose_name='性别',default=1)
    phone = models.CharField(max_length=20,blank=True,verbose_name='电话')
    avatar = models.ImageField(blank=True, upload_to='images/',default='images/1.jpg',verbose_name='头像')
    signature = models.CharField(max_length=128, default='This guy is too lazy to leave anything here!')
class Meta(AbstractUser.Meta):
        pass