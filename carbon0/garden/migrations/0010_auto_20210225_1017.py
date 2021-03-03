# Generated by Django 3.1.1 on 2021-02-25 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0009_auto_20210224_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaf',
            name='status',
            field=models.CharField(choices=[('M', 'Moderate'), ('H', 'Heathy'), ('U', 'Unhealthy')], default='M', help_text='The healthiness of this leaf.', max_length=1),
        ),
    ]