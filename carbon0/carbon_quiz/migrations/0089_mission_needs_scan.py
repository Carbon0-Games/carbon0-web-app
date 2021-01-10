# Generated by Django 3.1.1 on 2021-01-08 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_quiz', '0088_remove_mission_needs_scan'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='needs_scan',
            field=models.BooleanField(default=False, help_text='Is the mission completed by scanning a QR code.'),
        ),
    ]