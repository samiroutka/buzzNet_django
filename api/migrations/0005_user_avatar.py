# Generated by Django 4.2.4 on 2023-10-30 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_user_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='buzz_net/avatars'),
        ),
    ]
