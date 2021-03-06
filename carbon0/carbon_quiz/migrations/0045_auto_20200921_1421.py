# Generated by Django 3.1.1 on 2020-09-21 18:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carbon_quiz", "0044_auto_20200921_1418"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mission",
            name="links",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(blank=True, max_length=300, null=True),
                blank=True,
                help_text="Links the user can click to complete the mission.Every alternating item is a website link, the other is its name.",
                null=True,
                size=6,
            ),
        ),
    ]
