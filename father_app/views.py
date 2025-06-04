from django.shortcuts import render, get_object_or_404
from .models import PoetryBook, Poem, MusicAlbum, Track


def index(request):
    return render(request, 'father_app/index.html')


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
# Поэзия
def book_list(request):
    books = PoetryBook.objects.all().order_by('-year')
    return render(request, 'father_app/poetry/book_list.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(PoetryBook, pk=book_id)
    return render(request, 'father_app/poetry/book_detail.html', {'book': book})


def poem_detail(request, book_id, poem_id):
    poem = get_object_or_404(Poem, pk=poem_id, book_id=book_id)
    poems = list(poem.book.poems.all())
    current_index = next(i for i, p in enumerate(poems) if p.id == poem.id)

    return render(request, 'father_app/poetry/poem_detail.html', {
        'book': poem.book,
        'poem': poem,
        'prev_poem': poems[current_index - 1] if current_index > 0 else None,
        'next_poem': poems[current_index + 1] if current_index < len(poems) - 1 else None,
    })


# Музыка
def album_list(request):
    albums = MusicAlbum.objects.all().order_by('-year')
    return render(request, 'father_app/music/album_list.html', {'albums': albums})


def album_detail(request, album_id):
    album = get_object_or_404(MusicAlbum, pk=album_id)
    return render(request, 'father_app/music/album_detail.html', {'album': album})


# Обработчик 404
def page_not_found(request, exception):
    return render(request, 'father_app/404.html', status=404)