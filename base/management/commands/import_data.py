import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from base.models import Topic, Room, Message, User

Models = {
    Topic: 'base_topic.csv',
    Room: 'base_room.csv',
    Room.participants.through: 'base_room_participants.csv',
    Message: 'base_message.csv',
}


class Command(BaseCommand):
    help = 'Загрузка данных из csv файлов'

    def handle(self, *args, **options):
        for model, csv_files in Models.items():
            with open(
                f'{settings.BASE_DIR}/data/{csv_files}',
                'r',
                encoding='utf-8-sig'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader
                )
            self.stdout.write(
                f'Данные для таблицы {model.__name__} успешно загружены')
        return('База данных успешно загружена.')