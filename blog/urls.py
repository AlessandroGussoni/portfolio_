from django.urls import path
from .views import GetPosts, GetPost, GetPaginatedPosts

urlpatterns = [
    path('get-posts', GetPosts.as_view()),
    path('get-post', GetPost.as_view()),
    path('get-pag-posts', GetPaginatedPosts.as_view())
]