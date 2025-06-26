from django.core.management.base import BaseCommand
from father_app.models import PoetryBook, Poem
import json
from pathlib import Path
from django.core.files import File


class Command(BaseCommand):
    help = 'Импорт стихов из JSON файла'

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str, help='Путь к JSON файлу')

    def handle(self, *args, **kwargs):
        json_path = Path(kwargs['json_path'])

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Создаем книгу
        book = PoetryBook.objects.create(
            title=data['title'],
            year=data['year'],
            author=data.get('author', 'Лабытнанги')
        )

        # Загружаем обложку
        cover_path = Path(data['cover'])
        with cover_path.open('rb') as img:
            book.cover.save(cover_path.name, File(img))

        # Создаем стихи
        for poem_data in data['poems']:
            Poem.objects.create(
                book=book,
                title=poem_data['title'],
                content=poem_data['content'],
                order=poem_data.get('order', 0)
            )

        self.stdout.write(f'Успешно импортировано: {book.title}')