from django.conf.urls import url
from groups import views

app_name = 'groups'

urlpatterns = [
    url(r'^$',views.GroupList.as_view(), name='group_list'),
    url(r'^(?P<pk>\d+)/$', views.GroupDetailView.as_view(), name='group_detail'),
    url(r'^(?P<pk>\d+)/message/$', views.add_message_to_group, name='message_create'),
    url(r'^(?P<pk>\d+)/request/$', views.send_request_to_group, name='send_request'),
    url(r'^request_list/$', views.RequestListView.as_view(), name='request_list'),
    url(r'^request/(?P<pk>\d+)/accept/$',views.request_accept, name='request_accept'),
    url(r'^request/(?P<pk>\d+)/reject/$', views.request_reject, name='request_reject'),


]