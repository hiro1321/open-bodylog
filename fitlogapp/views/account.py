from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
import random

from ..models import Profile
from ..services import account_service

# ssl._create_default_https_context = ssl._create_unverified_context
User = get_user_model()
ACCOUNTS_DIR = "fitlogapp/accounts/"


def signup(request):
    """
    ユーザー登録1のview
    メールアドレスチェックと認証メール送信を行う
    """
    # TODO:user名に使える文字をあるアルファベットと_のみにする
    # TODO:user名のほかに別名を登録できるようにする
    # TODO:メールアドレスが登録済みの場合はエラーメッセージが表示されるようにする
    # TODO:退会の機能を追加

    if request.method != "POST":
        return render(request, f"{ACCOUNTS_DIR}signup.html")

    email = request.POST.get("email")
    password = request.POST.get("password")

    if account_service.check_email_exists(email):
        messages.error(request, "対象のメールアドレスは登録済みです。")

    if len(messages.get_messages(request)) >= 1:
        return render(request, f"{ACCOUNTS_DIR}signup.html")

    user = User.objects.create_user(email=email, password=password)
    verification_code = f"{random.randint(100000, 999999)}"
    user.verification_code = verification_code
    user.verification_code_created_at = timezone.now()
    user.save()

    with SMTP(
        EMAIL_HOST,
        EMAIL_PORT,
    ) as server:
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

        msg = MIMEText(
            f"Open body logのサービスをご利用いただき、誠にありがとうございます。\n"
            f"以下の6桁の認証コードを、所定の認証ページにご入力ください。\n"
            f"このコードは安全のため30分間で無効になりますので、お早めにお手続きください。\n\n"
            f"■ 認証コード: {verification_code}\n\n"
            f"※万が一このメールに心当たりがない場合は、恐れ入りますが破棄してください。\n\n"
            f"引き続き、よろしくお願いいたします。\n",
            "plain",
            "utf-8",
        )
        msg["Subject"] = "アカウント認証のお手続き"
        msg["From"] = EMAIL_HOST_USER
        msg["To"] = email
        server.send_message(msg)

    context = {"email": user.email}
    return render(request, f"{ACCOUNTS_DIR}verify_code_page.html")


def verify_email(request, verification_code):
    """メール認証のview"""
    user = User.objects.filter(verification_code=verification_code).first()
    if user and not user.is_email_verified:
        if (timezone.now() - user.verification_code_created_at).days < 1:
            user.is_email_verified = True
            user.save()
            login(request, user)
            messages.success(
                request,
                "メールアドレスの認証に成功しました。ユーザー情報を登録してください。",
            )
            return redirect("user_register")
    return render(request, f"{ACCOUNTS_DIR}verify_email_fail.html")


def user_login(request):
    """ログインのview"""
    # TODO:password再設定の機能を追加
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("my_page")
        else:
            messages.error(request, "ユーザー名またはパスワードが正しくありません。")
    return render(request, f"{ACCOUNTS_DIR}login.html")


def user_logout(request):
    """ログアウトのview"""
    logout(request)
    return redirect("top_page")


@login_required
def user_register(request):
    """ユーザー情報登録ページ"""
    # POST以外の場合
    if request.method != "POST":
        return render(request, f"{ACCOUNTS_DIR}user_register.html")

    # POSTの場合
    username = request.POST.get("user_name", "")
    profile_bio = request.POST.get("profile_bio", "")

    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.bio = profile_bio
    profile.save()

    # 入力バリデーション
    if account_service.is_username_taken(username):
        messages.error(
            request, "同じ名前のユーザーが存在します。別のユーザ名を入力してください。"
        )
    if not username:
        messages.error(request, "ユーザー名を入力してください。")

    # エラーが存在する場合はユーザー登録ページへ戻る
    if len(messages.get_messages(request)) >= 1:
        context = {"user_name": username, "profile_bio": profile_bio}
        return render(request, f"{ACCOUNTS_DIR}user_register.html", context)

    # ユーザー登録後にmypageへリダイレクト
    request.user.custom_username = username
    request.user.save()
    return redirect("my_page")
