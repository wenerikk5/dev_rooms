# Generated by Django 4.1.7 on 2023-04-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_room_description_alter_room_host_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, upload_to='base/', verbose_name='Image'),
        ),
    ]