# Generated by Django 4.2.13 on 2024-07-22 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_userfollowing_accept_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfollowing',
            unique_together={('follower_id', 'followee_id')},
        ),
    ]
