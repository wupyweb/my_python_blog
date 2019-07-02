from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'blog'
urlpatterns = [
    # post views
    path('', views.article_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.article_list, name='post_list_by_tag'),
    path('about/', views.about, name='blog_about'),
    path('search/', views.search, name='blog_search'),
    path('mdeditor/', include('mdeditor.urls')),
    path('archive/', views.archive, name='archive')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
