# Generated by Django 5.0.4 on 2024-05-11 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitlogapp', '0006_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodyweight',
            name='body_weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='体重'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(max_length=100, verbose_name='トレーニング種目名'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='本文'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='投稿日'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/', verbose_name='イメージ'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, verbose_name='自己紹介文'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/', verbose_name='イメージ'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(verbose_name='日付'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='reps',
            field=models.PositiveIntegerField(verbose_name='rep数'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='weight',
            field=models.FloatField(verbose_name='重量'),
        ),
    ]
