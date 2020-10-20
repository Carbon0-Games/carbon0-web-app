# Generated by Django 3.1.1 on 2020-10-18 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_quiz', '0058_auto_20201018_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='good_response',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], default=1, help_text='Response that says the user is already doing well in this aspect of their carbon footprint.'),
        ),
    ]