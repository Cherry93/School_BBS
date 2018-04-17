from django.db import models
from posts.models import Post
from users.models import User
from DjangoUeditor.models import UEditorField
# Create your models here.


class Comment(models.Model):
    """评论"""
    user = models.ForeignKey(User)
    text = UEditorField(width=900, height=200, imagePath="images/",
                           filePath="images/", verbose_name=u"评论内容",blank=True,default='评论')
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)

    def __str__(self):
        return self.text[:20]


class CommentReply(models.Model):
    """回复"""
    content = models.TextField()
    comment = models.ForeignKey(Comment, related_name='comment_replies')
    author = models.ForeignKey(User, related_name='user_comment_replies', null=True, blank=True,
                               on_delete=models.SET_NULL)
    replay_user = models.ForeignKey(User, related_name='user_replied', null=True, blank=True, on_delete=models.SET_NULL)
    replay_time = models.DateTimeField()
    # review = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0}->{1}'.format(self.author, self.replay_user)