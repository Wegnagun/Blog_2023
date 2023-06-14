from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    """ Менеджер опубликованный постов. """

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """ Модель постов. """

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=100, verbose_name='Заголовок',)
    slug = models.SlugField(max_length=50)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='Автор поста',
    )
    body = models.TextField(verbose_name='Текст поста')
    publish = models.DateTimeField(
        default=timezone.now,
        verbose_name='Опубликован',
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус поста',
    )

    objects = models.Manager()  # менеджер по умолчанию
    published = PublishedManager()  # менеджер возврата опубликованных постов

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
