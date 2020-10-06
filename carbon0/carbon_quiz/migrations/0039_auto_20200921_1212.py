# Generated by Django 3.1.1 on 2020-09-21 16:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_quiz', '0038_auto_20200921_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='links',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100, null=True), help_text='Links the user can click to complete the mission.', null=True, size=10), null=True, size=3),
        ),
    ]
