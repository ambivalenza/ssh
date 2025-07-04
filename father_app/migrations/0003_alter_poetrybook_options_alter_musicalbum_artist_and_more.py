# Generated by Django 5.2.2 on 2025-06-04 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('father_app', '0002_musicalbum_poetrybook_remove_song_album_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poetrybook',
            options={'ordering': ['-year'], 'verbose_name': 'Книга стихов', 'verbose_name_plural': 'Книги стихов'},
        ),
        migrations.AlterField(
            model_name='musicalbum',
            name='artist',
            field=models.CharField(default='Сергей Шорников', max_length=200, verbose_name='Исполнитель'),
        ),
        migrations.AlterField(
            model_name='musicalbum',
            name='cover',
            field=models.ImageField(upload_to='music/covers/', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='poetrybook',
            name='author',
            field=models.CharField(default='Сергей Шорников', max_length=200, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='poetrybook',
            name='cover',
            field=models.ImageField(upload_to='books/covers/', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='poetrybook',
            name='pdf_file',
            field=models.FileField(upload_to='books/pdfs/', verbose_name='PDF файл'),
        ),
    ]
