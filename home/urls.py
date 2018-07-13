from django.conf.urls import url
from home import views

app_name = 'home'

urlpatterns =[
    url('^$', views.Index.as_view(), name='index')
]