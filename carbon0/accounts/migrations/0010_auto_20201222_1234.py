# Generated by Django 3.1.1 on 2020-12-22 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_profile_photos_are_accurate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="photos_are_accurate",
            field=models.BooleanField(
                blank=True,
                help_text="We can only save the planet if your image is actually of a sign!",
                null=True,
            ),
        ),
    ]
