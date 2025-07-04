# Generated by Django 5.2.2 on 2025-06-26 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('father_app', '0005_alter_musicalbum_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poetrybook',
            options={'verbose_name': 'Книга стихов', 'verbose_name_plural': 'Книги стихов'},
        ),
        migrations.RemoveField(
            model_name='poetrybook',
            name='created_at',
        ),
        migrations.AddField(
            model_name='poetrybook',
            name='page_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество страниц'),
        ),
        migrations.DeleteModel(
            name='Poem',
        ),
    ]
