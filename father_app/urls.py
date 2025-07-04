from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'father_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('music/', views.album_list, name='music_album_list'),
    path('music/<int:album_id>/', views.album_detail, name='music_album_detail'),
    path('music/<int:album_id>/track/<int:track_id>/', views.track_detail, name='music_track_detail'),
]

# Добавляем обслуживание медиа файлов для разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'father_app.views.page_not_found'