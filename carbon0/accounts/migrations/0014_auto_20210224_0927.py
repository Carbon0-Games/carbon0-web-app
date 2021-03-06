# Generated by Django 3.1.1 on 2021-02-24 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0013_remove_profile_plant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="diet_sign_photo",
            field=models.ImageField(
                blank=True,
                help_text="Your sign for Diet Missions.",
                null=True,
                upload_to="accounts/static/accounts/images",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="mugshot",
            field=models.ImageField(
                blank=True,
                help_text="User profile image",
                null=True,
                upload_to="accounts/static/accounts/images",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="offsets_sign_photo",
            field=models.ImageField(
                blank=True,
                help_text="Your sign for Airline-Utilities Missions.",
                null=True,
                upload_to="accounts/static/accounts/images",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="recycling_sign_photo",
            field=models.ImageField(
                blank=True,
                help_text="Your sign for Recycling Missions.",
                null=True,
                upload_to="accounts/static/accounts/images",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="transit_sign_photo",
            field=models.ImageField(
                blank=True,
                help_text="Your sign for Transit Missions.",
                null=True,
                upload_to="accounts/static/accounts/images",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="utilities_sign_photo",
            field=models.ImageField(
                blank=True,
                help_text="Your sign for Utilities Missions.",
                null=True,
                upload_to="accounts/static/accounts/images",
            ),
        ),
    ]
