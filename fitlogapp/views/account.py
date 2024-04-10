# accounts/views.py

from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from fitlogproject.settings import (
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    BASE_URL,
)
from smtplib import SMTP
from email.mime.text import MIMEText
import ssl


ssl._create_default_https_context = ssl._create_unverified_context
User = get_user_model()


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(
                email=email, custom_username=user_name, password=password
            )
            verification_code = get_random_string(length=32)
            user.verification_code = verification_code
            user.verification_code_created_at = timezone.now()
            user.save()
            verification_link = f"{BASE_URL}/verify/{verification_code}/"

            with SMTP(
                EMAIL_HOST,
                EMAIL_PORT,
            ) as server:
                server.starttls()
                server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

                msg = MIMEText(
                    f"以下のリンクをクリックしてメールアドレスを確認してください: {verification_link}",
                    "plain",
                    "utf-8",
                )
                msg["Subject"] = "メールアドレスの確認"
                msg["From"] = EMAIL_HOST_USER
                msg["To"] = email
                server.send_message(msg)

            return render(request, "accounts/register_done.html")
    return render(request, "accounts/register.html")


def verify_email(request, verification_code):
    user = User.objects.filter(verification_code=verification_code).first()
    if user and not user.is_email_verified:
        if (timezone.now() - user.verification_code_created_at).days < 1:
            user.is_email_verified = True
            user.save()
            return render(request, "accounts/verify_email_success.html")
    return render(request, "accounts/verify_email_fail.html")


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home_page")
        else:
            messages.error(request, "ユーザー名またはパスワードが正しくありません。")
    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("top_page")
