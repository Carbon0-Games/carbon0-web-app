# Generated by Django 3.1.1 on 2021-02-26 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("garden", "0011_auto_20210226_1307"),
    ]

    operations = [
        migrations.AlterField(
            model_name="machinelearning",
            name="architecture",
            field=models.FileField(
                help_text="JSON instructions for how to constrcut                   the underlying neural network.",
                null=True,
                upload_to="garden/static/garden/neural_networks/architecture",
            ),
        ),
        migrations.AlterField(
            model_name="machinelearning",
            name="weights",
            field=models.FileField(
                help_text="Hadoop instructions for what weights and biases                   to give the underlying neural network.",
                null=True,
                upload_to="garden/static/garden/neural_networks/parameters",
            ),
        ),
    ]
