from django.shortcuts import render, get_object_or_404, redirect
from ..services import chart_service
from ..models import CustomUser, Profile, Post, Follow
from ..forms import ProfileForm
from ..objects.profile_dto import ProfileDto
from ..objects.chart_request_dto import ChartRequestDto
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


USER_DIR = "fitlogapp/user/"


@login_required
def my_page(request):
    """マイページ情報を表示"""
    context = {}
    context["posts"] = Post.objects.order_by("-created_at")

    return render(request, f"{USER_DIR}my_page.html", context)


@login_required
def show_user(request, custom_username):
    """対象userの情報を表示"""
    user = CustomUser.objects.get(custom_username=custom_username)

    # TODO;対象userが存在しない場合のエラーハンドリング
    context = {}
    context["posts"] = Post.objects.filter(user=user).order_by("-created_at")

    profile_dto = ProfileDto(user)
    context["profile_dto"] = profile_dto.to_dict

    chart_request_dto = ChartRequestDto()
    chart_request_dto.user_id = user.id
    context["line_config"] = chart_service.create_chart_config(chart_request_dto)

    context["user_id"] = user.id

    return render(request, USER_DIR + "show_user.html", context)


@require_POST
def create_chert(request):
    """リクエストをもとにチャート情報を返す"""
    data = json.loads(request.body)
    chart_request_dto = ChartRequestDto()
    chart_request_dto.user_id = data.get("userId")
    chart_request_dto.period = data.get("period")
    chart_request_dto.set_value = data.get("setValue")
    if chart_request_dto.set_value == "set":
        chart_request_dto.rep_input = data.get("repInput")
        chart_request_dto.set_input = data.get("setInput")
    line_config = chart_service.create_chart_config(chart_request_dto)

    return JsonResponse({"line_config": line_config})


@login_required
def edit_profile(request):
    """プロフィール情報を編集"""
    user_profile = Profile.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("my_page")
    else:
        if user_profile:
            form = ProfileForm(instance=user_profile)
        else:
            form = ProfileForm()

    return render(request, USER_DIR + "edit_profile.html", {"form": form})


@login_required
def toggle_follow(request, user_id):
    """対象ユーザーをフォロー/解除を切り替えて更新"""
    follow_user = CustomUser.objects.get(id=request.user.id)
    followed_user = CustomUser.objects.get(id=user_id)

    # TODO:自ユーザーへのフォローを除外
    if Follow.objects.filter(
        follower=follow_user, followed_user=followed_user
    ).exists():
        Follow.objects.filter(
            follower=follow_user, followed_user=followed_user
        ).delete()
        is_following = False
    else:
        Follow.objects.create(follower=follow_user, followed_user=followed_user)
        is_following = True

    return JsonResponse({"is_following": is_following})


@login_required
def following_users(request, user_id):
    """フォローしているユーザーの一覧を出力"""
    user = CustomUser.objects.get(id=user_id)
    follows = user.following.all()
    profile_list = [ProfileDto(follow.followed_user) for follow in follows]
    context = {"profile_list": profile_list}

    return render(request, USER_DIR + "profile_list.html", context)


@login_required
def followers_users(request, user_id):
    """フォローされているユーザーの一覧を出力"""
    user = CustomUser.objects.get(id=user_id)
    follows = user.followers.all()
    profile_list = [ProfileDto(follow.follower) for follow in follows]
    context = {"profile_list": profile_list}

    return render(request, USER_DIR + "profile_list.html", context)


@login_required
def liked_users(request, post_id):
    """対象の投稿にいいねしたユーザーのプロフィール情報を表示"""
    post = Post.objects.get(id=post_id)
    liked_users = post.likes.all()
    profile_list = [ProfileDto(user) for user in liked_users]
    context = {"profile_list": profile_list}

    # TODO:profile_listを呼ぶときはh2タグの中身を動的に変更
    return render(request, USER_DIR + "profile_list.html", context)
