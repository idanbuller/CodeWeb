from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post


class PostCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'testuser@test.com', 'testpass')

    def test_post_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post-create'), {'title': 'Test title', 'content': 'Test content'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test title')
        self.assertEqual(post.content, 'Test content')
        self.assertEqual(post.author, self.user)