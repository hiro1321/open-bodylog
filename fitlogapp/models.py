from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, custom_username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です。")
        email = self.normalize_email(email)
        user = self.model(email=email, custom_username=custom_username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, custom_username=None, password=None, **extra_fields
    ):
        user = self.create_user(
            email, custom_username=custom_username, password=password, **extra_fields
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_email_verified = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        "メールアドレス",
        unique=True,
    )
    custom_username = models.CharField("ユーザー名", max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField("メール認証フラグ", default=False)
    verification_code = models.CharField(
        "認証コード", max_length=100, blank=True, null=True
    )
    verification_code_created_at = models.DateTimeField(
        "認証コード作成日時", blank=True, null=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["custom_username"]

    def __str__(self):
        return self.email


class MusclePart(models.Model):
    part_name = models.CharField("部位", max_length=100)


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscle_part = models.ForeignKey(MusclePart, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.id}_{self.user.custom_username} - {self.exercise.name} on {self.date}"


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.custom_username}'s Profile"


class BodyWeight(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body_weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    date = models.DateField()

    def __str__(self):
        return f"{self.user.custom_username}'s Body weight"


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"{self.user.custom_username} - {self.created_at}"


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.custom_username} - {self.post}"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.custom_username} liked {self.post}"


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, related_name="following", on_delete=models.CASCADE
    )
    followed_user = models.ForeignKey(
        CustomUser, related_name="followers", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.follower.custom_username} follows {self.followed_user.custom_username}"
