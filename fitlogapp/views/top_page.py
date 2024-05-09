from django.shortcuts import render


def top_page(request):
    # TODO:トップページにサービス概要を記載
    return render(request, "fitlogapp/top_page.html")
