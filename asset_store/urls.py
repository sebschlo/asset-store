from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^apiv1/', include('assets.urls')),
    url(r'^admin/', admin.site.urls),
]
