# Generated by Django 5.1 on 2024-12-10 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_alter_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='img',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
