from django.conf.urls import url
from iot_hub import views

urlpatterns = [
    url(r'^api/datasource/$', views.datasource_list),
    url(r'^api/(?P<uuid>[^/]+)/$', views.datasource_detail),
]