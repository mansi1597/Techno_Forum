from django.conf.urls import url
from posts import views
from django.views.decorators.http import require_POST
app_name = "posts"


urlpatterns = [
    url(r'^newsfeed/(?P<pk>\d+)$', views.list_and_create, name='list_and_create'),
    url(r'^(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),
    url(r'^(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
    url(r'^(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^comment/(?P<pk>\d+)/new/$', require_POST(views.add_comment_to_post), name='comment_create'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.CommentDeleteView.as_view(), name='comment_remove'),
]