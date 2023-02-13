from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # text editing
    path('tinymce/', include('tinymce.urls')),
    # APIs
    path('api/', include('blog.urls')),

    path('', views.index, name='index'),

    path('blog/page/<pagenum>', views.index, name='blog')
]
