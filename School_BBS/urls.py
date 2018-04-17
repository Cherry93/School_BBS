"""School_BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from users import views
from posts import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls')),
    url(r'^', include('posts.urls')),
    url(r'^', include('comments.urls')),
    # 将 auth 应用中的 urls 模块包含进来
    url(r'^users/', include('django.contrib.auth.urls')),
    # 别忘记在顶部引入 views 模块
    url(r'^$', views.index, name='index'),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


