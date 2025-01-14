# Generated by Django 5.0.4 on 2024-09-15 10:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fitlogapp", "0007_alter_bodyweight_body_weight_alter_exercise_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="change_password_code",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="パスワード変更認証コード"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="change_password_code_created_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="パスワード変更認証コード作成日時"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="change_password_flg",
            field=models.BooleanField(default=False, verbose_name="パスワード変更フラグ"),
        ),
    ]