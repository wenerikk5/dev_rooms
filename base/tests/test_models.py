from django.contrib.auth import get_user_model
from django.test import TestCase

from base.models import Topic, Room, Message


User = get_user_model()


class RoomModelTest(TestCase):
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
        cls.room.participants.set([cls.user,])

    def test_verbose_name(self):
        room = RoomModelTest.room
        field_verboses = {
            'host': 'Host user name',
            'head': 'Room name',
            'description': 'Description',
            'participants': 'Participants',
            'topic': 'Topic',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    room._meta.get_field(field).verbose_name, expected_value
                )

    def test_models_have_correct_object_names(self):
        room = RoomModelTest.room
        expected_object_name = room.head
        self.assertEqual(expected_object_name, str(room))


class MessageModelTest(TestCase):
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
        cls.room.participants.set([cls.user,])
        cls.message = Message.objects.create(
            body='Test' * 50,
            author=cls.user,
            room=cls.room,
        )

    def test_correct_length_of_object_body(self):
        message = self.message
        expected_object_name = ('Test' * 50)[:50]
        self.assertEqual(expected_object_name, str(message))
