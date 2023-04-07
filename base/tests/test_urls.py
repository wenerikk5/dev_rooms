from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from base.models import Topic, Room, Message


User = get_user_model()


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.topic = Topic.objects.create(
            name='Python'
        )
        cls.room = Room.objects.create(
            host=cls.user,
            head='Test Room',
            description='Test Room description',
            topic=cls.topic,
        )
        cls.room.participants.set([cls.user, ])
        cls.message = Message.objects.create(
            body='Test' * 50,
            author=cls.user,
            room=cls.room,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(StaticURLTests.user)

    # Check URLs
    def test_url_exists_unauthorized(self):
        url_names_unauthorized = {
            '/': '/',
            '/login/': '/login/',
            '/register/': '/register/',
            '/room/1/': '/room/1/',
        }
        for url, address in url_names_unauthorized.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_url_exists_authorized(self):
        url_names_authorized = {
            '/room/1/edit/': '/room/1/edit/',
            '/room/1/delete/': '/room/1/delete/',
        }
        for url, address in url_names_authorized.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_urls_redirects(self):
        url_names_redirects = {
            '/room/1/delete/': '/login/?next=/room/1/delete/',
            '/room/1/edit/': '/login/?next=/room/1/edit/',
        }
        for url, redirect in url_names_redirects.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertRedirects(response, redirect)

    # Check Templates
    def test_urls_uses_correct_templates(self):
        template_url_names_authorized = {
            '/room/1/edit/': 'base/create_room.html',
            '/room/1/delete/': 'base/delete.html',
            '/delete-message/1/': 'base/delete.html',
        }
        template_url_names_unauthorized = {
            '/': 'base/index.html',
            '/login/': 'base/login.html',
            '/register/': 'base/register.html',
            '/profile/1/': 'base/profile.html',
            '/room/1/': 'base/room.html',
        }
        for address, template in template_url_names_authorized.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

        for address, template in template_url_names_unauthorized.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
