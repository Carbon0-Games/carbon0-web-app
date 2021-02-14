# Generated by Django 3.1.1 on 2021-02-14 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carbon_quiz", "0089_mission_needs_scan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="achievement",
            name="completion_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="Date mission was accomplished", null=True
            ),
        ),
    ]
