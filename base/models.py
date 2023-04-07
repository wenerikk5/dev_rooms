from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Topic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Message(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created',]

    def __str__(self):
        return self.body[0:50]


class Room(models.Model):
    host = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Host user name',
    )
    head = models.CharField('Room name', max_length=80)
    description = models.TextField('Description', null=True, blank=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Topic',
    )
    image = models.ImageField(
        'Image',
        upload_to='base/',
        blank=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='rooms',
        blank=True,
        verbose_name='Participants'
    )
    link = models.URLField('Link to source page', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-head']

    def __str__(self):
        return self.head
