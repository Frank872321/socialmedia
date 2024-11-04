# Generated by Django 5.1 on 2024-10-20 00:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content',
            new_name='body',
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='dweets', to=settings.AUTH_USER_MODEL),
        ),
    ]
