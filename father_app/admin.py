from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import PoetryBook, MusicAlbum, Track

@admin.register(PoetryBook)
class PoetryBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'get_year', 'page_count', 'pdf_link']
    readonly_fields = ['page_count', 'pdf_preview']
    fields = ['title', 'author', 'year', 'cover', 'pdf_file', 'page_count', 'pdf_preview']
    list_filter = ['author']  # Или другие существующие поля

    def get_year(self, obj):
        return obj.year

    get_year.short_description = 'Год'
    get_year.admin_order_field = 'year'  # Для сортировки

    def pdf_link(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">Открыть PDF</a>', obj.pdf_file.url)
        return "-"

    pdf_link.short_description = "PDF"

    def pdf_preview(self, obj):
        if obj.pdf_file:
            return format_html(
                '<iframe src="{}#toolbar=0&view=FitH" style="width:100%; height:500px;"></iframe>',
                obj.pdf_file.url
            )
        return "PDF не загружен"

    pdf_preview.short_description = "Предпросмотр PDF"

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
    list_filter = ['year', 'month', 'artist']
    search_fields = ['title', 'artist']
    inlines = [TrackInline]

    def tracks_link(self, obj):
        count = obj.tracks.count()
        url = reverse('admin:father_app_track_changelist') + f'?album__id__exact={obj.id}'
        return format_html('<a href="{}">Треки ({})</a>', url, count)
    tracks_link.short_description = "Треки"

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'album_link', 'order', 'duration_formatted']
    list_filter = ['album']
    search_fields = ['title']

    def album_link(self, obj):
        url = reverse('admin:father_app_musicalbum_change', args=[obj.album.id])
        return format_html('<a href="{}">{}</a>', url, obj.album.title)
    album_link.short_description = "Альбом"
    album_link.admin_order_field = 'album'

    def duration_formatted(self, obj):
        if obj.duration:
            total_seconds = int(obj.duration.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}:{seconds:02d}"
        return "--:--"
    duration_formatted.short_description = "Длительность"
    duration_formatted.admin_order_field = 'duration'