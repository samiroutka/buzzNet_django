# Generated by Django 4.2.4 on 2023-10-29 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribers', models.JSONField()),
                ('subscriptions', models.JSONField()),
            ],
        ),
    ]
