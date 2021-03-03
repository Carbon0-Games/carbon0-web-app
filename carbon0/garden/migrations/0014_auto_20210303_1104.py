# Generated by Django 3.1.1 on 2021-03-03 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0013_auto_20210303_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaf',
            name='image',
            field=models.ImageField(blank=True, help_text='Image of the leaf.', null=True, upload_to='garden/images'),
        ),
        migrations.AlterField(
            model_name='machinelearning',
            name='architecture',
            field=models.FileField(help_text='JSON instructions for how to constrcut                   the underlying neural network.', null=True, upload_to='garden/neural_networks/architecture'),
        ),
        migrations.AlterField(
            model_name='machinelearning',
            name='weights',
            field=models.FileField(help_text='Hadoop instructions for what weights and biases                   to give the underlying neural network.', null=True, upload_to='garden/neural_networks/parameters'),
        ),
    ]
