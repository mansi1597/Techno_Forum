from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^profile/(?P<pk>\d+)$', views.ProfileDetailView.as_view(), name='profile'),
    url(r'^profile/(?P<pk>\d+)/edit/$', views.profile_update, name='edit_profile'),
]