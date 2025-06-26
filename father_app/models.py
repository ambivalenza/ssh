from django.db import models
from django.urls import reverse


class PoetryBook(models.Model):
    title = models.CharField('Название', max_length=200)
    author = models.CharField('Автор', max_length=200, default="Сергей Шорников")
    year = models.IntegerField('Год издания')  # Это поле обязательно
    cover = models.ImageField('Обложка', upload_to='books/covers/')
    pdf_file = models.FileField('PDF файл', upload_to='books/pdfs/')
    page_count = models.PositiveIntegerField('Количество страниц', default=0)

    class Meta:
        verbose_name = 'Книга стихов'
        verbose_name_plural = 'Книги стихов'

    def save(self, *args, **kwargs):
        if not self.page_count and self.pdf_file:
            import PyPDF2
            try:
                with open(self.pdf_file.path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    self.page_count = len(reader.pages)
            except:
                pass
        super().save(*args, **kwargs)


class MusicAlbum(models.Model):
    title = models.CharField('Название', max_length=200)
    artist = models.CharField('Исполнитель', max_length=200, default="Сергей Шорников")
    month = models.PositiveSmallIntegerField(
        'Месяц публикации',
        null=True,
        blank=True,
        choices=[(i, i) for i in range(1, 13)],
        help_text='Месяц выпуска альбома (1-12)'
    )
    year = models.IntegerField('Год выпуска')
    cover = models.ImageField('Обложка', upload_to='music/covers/')
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', '-month']
        verbose_name = 'Музыкальный альбом'
        verbose_name_plural = 'Музыкальные альбомы'

    def __str__(self):
        return f"{self.title} ({self.year})"

    def get_absolute_url(self):
        return reverse('father_app:music:album_detail', args=[str(self.id)])

class Track(models.Model):
    album = models.ForeignKey(MusicAlbum, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField('Название', max_length=200)
    order = models.PositiveIntegerField('Порядковый номер', default=0)
    audio_file = models.FileField('Аудиофайл', upload_to='music/tracks/')
    duration = models.DurationField('Длительность', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'

    def __str__(self):
        return f"{self.order}. {self.title}"