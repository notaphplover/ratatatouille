from . import views
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
]
