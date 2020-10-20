# Generated by Django 3.1.1 on 2020-10-06 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carbon_quiz", "0053_mission_percent_carbon_sequestration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mission",
            name="percent_carbon_sequestration",
            field=models.FloatField(
                default=0.0,
                help_text="The percent of the user's carbon footprint that completing this mission will offset. Entered in as a float e.g. if the value entered here is 0.97, that means 97%.",
            ),
        ),
    ]