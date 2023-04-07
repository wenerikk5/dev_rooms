import shutil
import tempfile

from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from base.models import Topic, Room
from base.forms import RoomForm


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
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

    # @classmethod
    # def tearDownClass(cls):
    #     super().tearDownClass()
    #     shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(StaticURLTests.user)

    def test_create_room(self):
        rooms_count = Room.objects.count()

        form_data = {
            'host': StaticURLTests.user,
            'head': 'Room2',
            'description': 'Test description of Room 2',
            'topic': StaticURLTests.topic,
        }
        response = self.authorized_client.post(
            reverse('create-room'),
            data=form_data,
            follow=True
        )
        # Check redirect
        self.assertRedirects(response, reverse('home'))
        # Check quantity of rooms
        self.assertEqual(Room.objects.count(), rooms_count + 1)
        # Check new room is exists with added data
        self.assertTrue(
            Room.objects.filter(
                head='Room2',
                description='Test description of Room 2',
                host=1,
                topic=1,
            )
        )
