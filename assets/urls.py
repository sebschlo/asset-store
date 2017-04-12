from django.conf.urls import url
from assets import views

urlpatterns = [
    url(r'^assets/$', views.asset_list),
    url(r'^assets/(?P<pk>[0-9a-zA-Z_-]+)/$', views.asset_detail),
]