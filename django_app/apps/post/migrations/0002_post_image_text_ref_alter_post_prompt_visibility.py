# Generated by Django 4.2.13 on 2024-06-24 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image_text_ref',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='prompt_visibility',
            field=models.CharField(choices=[('PR', 'Private'), ('FO', 'Followers Only'), ('PU', 'Public')], default='PU', max_length=2),
        ),
    ]
