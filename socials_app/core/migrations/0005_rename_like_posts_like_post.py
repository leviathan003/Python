# Generated by Django 4.2.3 on 2023-07-26 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_like_posts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='like_posts',
            new_name='like_post',
        ),
    ]
