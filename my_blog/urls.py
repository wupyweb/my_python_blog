from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # post views
    path('', views.article_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.article_list, name='post_list_by_tag'),
    path('about/', views.about, name='blog_about'),
    path('search/', views.search, name='blog_search')
]
