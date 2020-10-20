# Generated by Django 3.1.1 on 2020-10-01 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("carbon_quiz", "0048_achievement_secret_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="achievement",
            name="profile",
            field=models.ForeignKey(
                help_text="The profile that owns this achievement.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="accounts.profile",
            ),
        ),
    ]