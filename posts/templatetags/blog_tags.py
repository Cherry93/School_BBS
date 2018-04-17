from django import template
from django.db.models import Count
from users.models import User
from ..models import Post, Category, Tag,Favorite,Like,Best
from comments.models import Comment
register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives(num=5):
    return Post.objects.dates('created_time', 'month', order='DESC')[:num]

@register.simple_tag
def archives2(num=5):
    return Post.objects.dates('created_time', 'day', order='DESC')[:num]

@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)

@register.simple_tag
def get_comments():
    return Comment.objects.annotate(num_comm=Count('user')).filter(num_comm__gt=0)

@register.simple_tag
def get_fav():
    return Favorite.objects.annotate(num_fav=Count('post')).filter(num_fav_gt=0)

@register.simple_tag
def get_like():
    return Like.objects.annotate(num_like=Count('post')).filter(num_like__gt=0)

@register.simple_tag
def get_best():
    return Best.objects.annotate(num_best=Count('post')).filter(num_best__gt=0)