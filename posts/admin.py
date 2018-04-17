from django.contrib import admin
from .models import Post,Tag,Category,Like,Favorite
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Favorite)