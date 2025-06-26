from django.shortcuts import render, get_object_or_404
from .models import MusicAlbum, Track, PoetryBook
import os
from django.http import JsonResponse
from django.conf import settings

def index(request):
    context = {
        'is_home': True
    }
    return render(request, 'father_app/index.html', context)


def debug_pdf(request, book_id):
    """Диагностическая view для проверки PDF файлов"""
    book = get_object_or_404(PoetryBook, pk=book_id)

    debug_info = {
        'book_title': book.title,
        'pdf_file_name': book.pdf_file.name if book.pdf_file else None,
        'pdf_url': book.pdf_file.url if book.pdf_file else None,
        'pdf_file_exists': bool(book.pdf_file and os.path.exists(book.pdf_file.path)) if book.pdf_file else False,
        'media_url': settings.MEDIA_URL,
        'media_root': settings.MEDIA_ROOT,
        'page_count': book.page_count,
    }

    if book.pdf_file:
        try:
            debug_info['pdf_file_path'] = book.pdf_file.path
            debug_info['pdf_file_size'] = os.path.getsize(book.pdf_file.path)
        except:
            debug_info['pdf_file_path'] = 'Файл не найден'
            debug_info['pdf_file_size'] = 0

    return JsonResponse(debug_info, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def book_list(request):
    books = PoetryBook.objects.all().order_by('-year')
    return render(request, 'father_app/poetry/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(PoetryBook, pk=book_id)
    return render(request, 'father_app/poetry/book_detail.html', {'book': book})

def book_view(request, book_id):
    book = get_object_or_404(PoetryBook, pk=book_id)
    page = request.GET.get('page', 1)

    # Рассчитываем диапазон страниц для разворота
    left_page = int(page)
    right_page = min(left_page + 1, book.page_count)

    return render(request, 'book_view.html', {
        'book': book,
        'left_page': left_page,
        'right_page': right_page,
        'total_pages': book.page_count,
    })


def track_detail(request, album_id, track_id):
    album = get_object_or_404(MusicAlbum, pk=album_id)
    track = get_object_or_404(Track, pk=track_id, album=album)
    tracks = list(album.tracks.all().order_by('order'))
    current_index = next(i for i, t in enumerate(tracks) if t.id == track.id)

    return render(request, 'father_app/music/track_detail.html', {
        'album': album,
        'track': track,
        'prev_track': tracks[current_index - 1] if current_index > 0 else None,
        'next_track': tracks[current_index + 1] if current_index < len(tracks) - 1 else None,
    })


# Музыка
def album_list(request):
    albums = MusicAlbum.objects.all().order_by('-year', '-month')
    return render(request, 'father_app/music/album_list.html', {'albums': albums})


def album_detail(request, album_id):
    album = get_object_or_404(MusicAlbum, pk=album_id)
    return render(request, 'father_app/music/album_detail.html', {'album': album})


# Обработчик 404
def page_not_found(request, exception):
    return render(request, 'father_app/404.html', status=404)
