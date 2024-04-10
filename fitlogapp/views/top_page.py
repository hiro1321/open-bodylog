from django.shortcuts import render


def top_page(request):
    return render(request, "fitlogapp/top_page.html")
