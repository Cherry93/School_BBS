from django.db import models
from users.models import User
# Create your models here.
from DjangoUeditor.models import UEditorField
from django.urls import reverse
# class Articles(models.Model):


class Post(models.Model):
    POST_FROM = {
        0: u'原创',
        1: u'转载',
    }
    title = models.CharField(max_length=256, default='new blog',verbose_name='标题')
    # content_html = models.TextField(null=True, blank=True,verbose_name='内容')
    content_html = UEditorField(width=940, height=600, imagePath="images/",
                           filePath="images/", verbose_name=u"文章内容",blank=True,default='images/1.jpg')

    # 创建时间上和更新时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modefied_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    # 定义外键关系
    author = models.ForeignKey(User, verbose_name='作者')
    category = models.ForeignKey('Category',blank=True ,verbose_name='话题')
    tags = models.ManyToManyField('Tag', blank=True,verbose_name='专栏')

    post_from = models.IntegerField(default=0, choices=POST_FROM.items(), verbose_name=u'文章来源')

    # 点赞，评论，收藏，转发数量
    like_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    favo_num = models.IntegerField(default=0)
    transmit_num = models.IntegerField(default=0)

    # 精华帖子模型，精华区分类和是否是精华帖
    best = models.ForeignKey('Best',blank=True,verbose_name='精华',null=True,default=None)
    best_act = models.IntegerField(default=0)

    # 阅读数
    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #/post/1/
        return reverse('posts:detail',kwargs={'pk':self.pk})


    class Meta:
        verbose_name_plural = '帖子'
        verbose_name = '帖子'


class Best(models.Model):       # 是否是精华帖子
    name = models.CharField(max_length=256)

    def __str__(self):
        return  self.name


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Like(models.Model):
    """点赞"""
    post = models.ForeignKey("Post")
    user = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return "%s likes post %s" % (self.user, self.post)


class Favorite(models.Model):
    """收藏"""
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return "%s collect post %s" % (self.user, self.post)

class Transmit(models.Model):
    """转发 """
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return "%s collect post %s" % (self.user, self.post)