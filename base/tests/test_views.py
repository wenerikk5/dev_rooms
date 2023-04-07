from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms

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

    # Check templates
    def test_page_uses_correct_template(self):
        # Excluding delete room and delete message (they use same template)
        template_page_names_authorized = {
            'base/index.html': reverse('home'),
            'base/profile.html': reverse('profile', kwargs={'pk': '1'}),
            'base/room.html': reverse('room', kwargs={'pk': '1'}),
            'base/create_room.html': reverse('create-room'),
        }
        template_page_names_unauthorized = {
            'base/login.html': reverse('login'),
            'base/register.html': reverse('register'),
        }
        for template, reverse_name in template_page_names_authorized.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

        for template, reverse_name in template_page_names_unauthorized.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Check context
    def test_home_page_context(self):
        response = self.guest_client.get(reverse('home'))
        # Check room details
        first_room = response.context['rooms'][0]
        room_head = first_room.head
        room_host_name = first_room.host.username
        room_topic_name = first_room.topic.name
        room_participant_name = first_room.participants.all()[0].username

        self.assertEqual(room_head, 'Test Room')
        self.assertEqual(room_host_name, 'auth')
        self.assertEqual(room_topic_name, 'Python')
        self.assertEqual(room_participant_name, 'auth')

        topics = response.context['topics']
        self.assertEqual(topics[0].name, 'Python')

        messages = response.context['rooms_messages']
        self.assertEqual(messages[0].body, ('Test' * 50))

    def test_room_update_page_context(self):
        response = self.authorized_client.get(reverse('edit-room', kwargs={'pk': '1'}))
        form_fields = {
            'head': forms.fields.CharField,
            'topic': forms.ModelChoiceField,
            'description': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
