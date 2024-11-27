# your_app/middleware.py

from django.shortcuts import redirect
from django.urls import reverse


class CustomUsernameRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ログインしていて、かつユーザー名が設定されていない場合
        if request.user.is_authenticated and not request.user.custom_username:
            # 設定ページへのURLがない場合のみリダイレクト
            if request.path != reverse("user_register"):
                return redirect("user_register")  # ユーザー名登録ページにリダイレクト

        response = self.get_response(request)
        return response
