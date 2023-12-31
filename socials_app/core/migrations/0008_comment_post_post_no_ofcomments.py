# Generated by Django 4.2.3 on 2023-07-27 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_following_followerscount_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment_post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('commenter', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='no_ofcomments',
            field=models.IntegerField(default=0),
        ),
    ]
