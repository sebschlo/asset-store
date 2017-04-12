from django.conf.urls import url
from assets import views

urlpatterns = [
    url(r'^assets/$', views.asset_list),
    url(r'^assets/(?P<class_name>[a-z]+)/classfilter/$', views.asset_classfilter),
    url(r'^assets/(?P<type_name>[a-z]+)/typefilter/$', views.asset_typefilter),
    url(r'^assets/(?P<pk>[0-9a-zA-Z_-]+)/$', views.asset_detail),
]