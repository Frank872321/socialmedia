# Generated by Django 5.1 on 2024-12-09 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='name',
            field=models.CharField(default='', max_length=250),
        ),
    ]
