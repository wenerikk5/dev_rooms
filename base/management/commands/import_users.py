import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(
            f'{settings.BASE_DIR}/data/base_user.csv',
            'r',
            encoding='utf-8-sig'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                user = User(
                    id=row['user_id'],
                    username=row['username'],
                    email=row['email'],
                    is_superuser=row['is_superuser'],
                    is_staff=row['is_staff'],
                    is_active=row['is_active']
                )
                user.set_password(row['password'])
                user.save()
        return (f'Users have been successfully added.')
