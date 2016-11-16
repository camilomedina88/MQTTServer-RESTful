from django.conf.urls import url
from iot_hub import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^datasources/(?P<uuid>[^/]+)/$', views.web_datasource),
    url(r'^api/datasources/$', views.datasource_list),
    url(r'^api/datasources/(?P<uuid>[^/]+)/$', views.datasource_detail),
    url(r'^api/variables/(?P<uuid>[^/]+)/$', views.var_value_detail),
    url(r'^api/variables/(?P<uuid>[^/]+)/$', views.var_value_detail),
]