from django.db import models
from django.urls import reverse

class PoetryBook(models.Model):
    title = models.CharField('Название', max_length=200)
    author = models.CharField('Автор', max_length=200, default="Сергей Шорников")
    year = models.IntegerField('Год издания')
    cover = models.ImageField('Обложка', upload_to='books/covers/')
    pdf_file = models.FileField('PDF файл', upload_to='books/pdfs/')
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_page_count = models.PositiveIntegerField('Количество страниц в PDF', default=0)

    def save(self, *args, **kwargs):
        if self.pdf_file and not self.pdf_page_count:
            import PyPDF2
            try:
                with open(self.pdf_file.path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    self.pdf_page_count = len(reader.pages)
            except:
                pass
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-year']
        verbose_name = 'Книга стихов'
        verbose_name_plural = 'Книги стихов'

    def __str__(self):
        return f"{self.title} ({self.year})"

    def get_absolute_url(self):
        return reverse('father_app:poetry:book_detail', args=[str(self.id)])

class Poem(models.Model):
    book = models.ForeignKey(PoetryBook, on_delete=models.CASCADE, related_name='poems')
    title = models.CharField('Название', max_length=200)
    content = models.TextField('Текст')
    order = models.PositiveIntegerField('Порядковый номер', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Стихотворение'
        verbose_name_plural = 'Стихотворения'

    def __str__(self):
        return f"{self.order}. {self.title}"

    def get_absolute_url(self):
        return reverse('father_app:poetry:poem_detail', args=[str(self.book.id), str(self.id)])

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