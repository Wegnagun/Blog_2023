from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Post


class PostTest(TestCase):
    """ Тесты модели поста. """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.ru',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Заголовок',
            slug='test-slug',
            author=self.user,
            body='test text',
            status='Published'
        )

    def test_post_create(self):
        """ Тест создания поста. """

        self.assertEqual(self.post.title, 'Заголовок')
        self.assertEqual(self.post.slug, 'test-slug')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.body, 'test text')
        self.assertEqual(self.post.status, Post.Status.PUBLISHED.label)
