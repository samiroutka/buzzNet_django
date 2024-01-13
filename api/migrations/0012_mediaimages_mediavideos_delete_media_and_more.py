# Generated by Django 4.2.4 on 2024-01-13 10:10

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_media'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(upload_to='api/media/images/')),
            ],
        ),
        migrations.CreateModel(
            name='MediaVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(upload_to='api/media/videos/')),
            ],
        ),
        migrations.DeleteModel(
            name='Media',
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, quality=1, scale=None, size=[500, 500], upload_to='api/media/avatars/'),
        ),
    ]
