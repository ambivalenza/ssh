from django.urls import path
from . import views

app_name = 'father_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('poetry/', views.book_list, name='book_list'),
    path('poetry/<int:book_id>/', views.book_detail, name='book_detail'),
    path('poetry/<int:book_id>/poem/<int:poem_id>/', views.poem_detail, name='poem_detail'),
    path('music/', views.album_list, name='music_album_list'),
    path('music/<int:album_id>/', views.album_detail, name='music_album_detail'),
    path('music/<int:album_id>/track/<int:track_id>/', views.track_detail, name='music_track_detail'),
]

handler404 = 'father_app.views.page_not_found'
