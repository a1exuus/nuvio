from django.contrib import admin
from django.urls import path
from django.urls import include
from nuvio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', views.index, name='index'),
]
