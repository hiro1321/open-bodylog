# Generated by Django 5.0 on 2024-04-09 15:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fitlogapp", "0003_alter_workout_date_follow_post_like_comment_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="body_weight",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True
            ),
        ),
    ]