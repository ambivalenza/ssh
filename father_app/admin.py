from django.contrib import admin
from django.utils.html import format_html
from .models import PoetryBook, Poem, MusicAlbum, Track
from django.urls import reverse
from django import forms

class PoemInline(admin.TabularInline):
    model = Poem
    extra = 1
    fields = ['order', 'title', 'content']

    def get_queryset(self, request):
        # Фикс для правильного отображения в админке
        qs = super().get_queryset(request)
        return qs.select_related('book')


@admin.register(PoetryBook)
class PoetryBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'year', 'poems_link']
    inlines = [PoemInline]

    def poems_link(self, obj):
        url = reverse('admin:father_app_poem_changelist') + f'?book__id__exact={obj.id}'
        return format_html('<a href="{}">Стихи ({})</a>', url, obj.poems.count())

    poems_link.short_description = "Стихотворения"

class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        widgets = {
            'content': forms.Textarea(attrs={'rows': 20, 'cols': 60, 'style': 'font-family: monospace;'}),
        }
        fields = '__all__'

@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    form = PoemForm
    list_display = ['title', 'book_link', 'order']
    list_filter = ['book']
    search_fields = ['title', 'content']

    def book_link(self, obj):
        url = reverse('admin:father_app_poetrybook_change', args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.title)

    book_link.short_description = "Книга"
    book_link.admin_order_field = 'book'


class TrackInline(admin.TabularInline):
    model = Track
    extra = 1
    fields = ('order', 'title', 'audio_player', 'duration')
    readonly_fields = ('audio_player', 'duration')

    def audio_player(self, obj):
        return format_html(
            '<audio controls src="{}" style="width: 250px;"></audio>',
            obj.audio_file.url
        ) if obj.audio_file else ''

    audio_player.short_description = "Прослушать"


@admin.register(MusicAlbum)
class MusicAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'year', 'month', 'tracks_link']
    list_filter = ['year', 'month', 'artist']  # можно фильтровать по месяцу
    search_fields = ['title', 'artist']

    def tracks_link(self, obj):
        url = reverse('admin:father_app_track_changelist') + f'?album__id__exact={obj.id}'
        return format_html('<a href="{}">Треки ({})</a>', url, obj.tracks.count())

    tracks_link.short_description = "Треки"


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'album_link', 'order']

    def album_link(self, obj):
        url = reverse('admin:father_app_musicalbum_change', args=[obj.album.id])
        return format_html('<a href="{}">{}</a>', url, obj.album.title)

    album_link.short_description = "Альбом"

    def duration_formatted(self, obj):
        return str(obj.duration).split('.')[0] if obj.duration else '--:--'

    duration_formatted.short_description = "Длительность"
    duration_formatted.admin_order_field = 'duration'