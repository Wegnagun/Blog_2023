from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .models import Post

User = get_user_model()


class PostTest(TestCase):
    """ Тесты модели поста. """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@email.ru',
            password='testpass123'
        )
        cls.post = Post.objects.create(
            title='Заголовок',
            slug='test-slug',
            author=cls.user,
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

    def test_posts_list_view(self):
        """ Тест представления списка постов. """

        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/list.html')

    # def test_posts_detail_view(self):
    #     """ Тест представления детализированного поста. """
    #
    #     response = self.client.get(
    #         reverse('blog:post_detail', args=[int(self.post.pk)])
    #     )
    #     no_response = self.client.get('/post/12345/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(no_response.status_code, 404)
    #     self.assertTemplateUsed(response, 'blog/detail.html')

