# Generated by Django 3.1.1 on 2020-12-03 17:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carbon_quiz", "0084_merge_20201201_1425"),
    ]

    operations = [
        migrations.AlterField(
            model_name="achievement",
            name="zeron_image_url",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(blank=True, max_length=100, null=True),
                blank=True,
                choices=[
                    (
                        [
                            "assets/glb-files/carrot180.glb",
                            "assets/usdz-files/carrot180.usdz",
                        ],
                        "Nature's Model",
                    ),
                    (
                        [
                            "assets/glb-files/wheel180.glb",
                            "assets/usdz-files/wheel180.usdz",
                        ],
                        "Wheel Model",
                    ),
                    (
                        [
                            "assets/glb-files/bin180.glb",
                            "assets/usdz-files/bin180.usdz",
                        ],
                        "Bin Model",
                    ),
                    (
                        [
                            "assets/glb-files/coin180.glb",
                            "assets/usdz-files/coin180.usdz",
                        ],
                        "Coin Model",
                    ),
                    (
                        [
                            "assets/glb-files/bulb180.glb",
                            "assets/usdz-files/bulb180.usdz",
                        ],
                        "Light Bulb Model",
                    ),
                    (
                        (["assets/glb-files/tree.glb", "assets/usdz-files/tree.usdz"],),
                        "Tree Zeron",
                    ),
                ],
                help_text="File paths to the 3D model in storage.",
                null=True,
                size=None,
            ),
        ),
    ]
