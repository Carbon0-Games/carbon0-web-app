# Generated by Django 3.1.1 on 2020-09-09 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_quiz', '0005_auto_20200908_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='completion_date',
            field=models.DateTimeField(blank=True, help_text='Date mission was accomplished', null=True),
        ),
    ]
