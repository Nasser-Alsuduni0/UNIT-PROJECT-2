# Generated by Django 5.2.4 on 2025-07-26 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_remove_review_user_review_reviewer_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='cover',
        ),
        migrations.AddField(
            model_name='book',
            name='cover_url',
            field=models.URLField(blank=True),
        ),
    ]
