from django.conf.urls import url
import posts.views as views
import posts.update as update
from .views import IndexView
app_name = 'posts'

urlpatterns = [
    url(r'^index/$', IndexView.as_view(), name='index'),
    # url(r'^index/', views.posts, name='index'),
    url(r'^categories/(?P<pk>\d+)/$', views.categories, name='categories'),
    url(r'^tags/(?P<pk>\d+)/$', views.tags, name='tags'),
    url(r'^best/(?P<pk>\d+)/$', views.tags, name='best'),
    url(r'^detail/(?P<pk>\d+)/$',views.detail, name='detail'),
    url(r'^add/$',views.add_post,name='add'),

    # 个人页面
    url(r'^profile/(\d+)$', views.profile, name='profile'),
    url(r'^favorite/(\d+)$', views.favorite, name='favorite'),
    url(r'^like/(\d+)$', views.like, name='like'),
    url(r'^comment/(\d+)$', views.comment, name='comment'),
    url(r'^tranmite/(\d+)$', views.transmite, name='tranmite'),


    url(r'^update_ava/$',update.update_ava,name='update_ava'),
    url(r'^update_name/$',update.update_name,name='update_name'),
    url(r'^update_ph/$',update.update_ph,name='update_ph'),
    url(r'^update_maj/$',update.update_maj,name='update_maj'),
    url(r'^update_qq/$',update.update_qq,name='update_qq'),
    url(r'^update_signature/$',update.update_signature,name='update_signature'),


    url(r'^favorite/$', views.add_favorite, name='favorite'),
    url(r'^like/$', views.add_like, name='like'),
    url(r'^transmit/$', views.add_transmit, name='transmit'),

    url(r'^search/$', views.search, name='search'),
]