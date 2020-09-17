# Generated by Django 3.1.1 on 2020-09-17 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_quiz', '0024_auto_20200917_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='zeron_image_url',
            field=models.CharField(blank=True, choices=[('assets/cartoon_carrot.glb', 'Carrot Model'), ('assets/Wheel.glb', 'Wheel Model'), ('assets/Bin.glb', 'Bin Model'), ('assets/coin.glb', 'Coin Model'), ('assets/Light bulb 1.glb', 'Light Bulb Model')], help_text='Path to the 3D model in storage.', max_length=100, null=True),
        ),
    ]
