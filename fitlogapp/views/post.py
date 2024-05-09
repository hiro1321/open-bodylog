from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..forms import PostForm
from ..models import Post


POST_DIR = "fitlogapp/post/"


@login_required
def create_post(request):
    """投稿を作成"""
    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect("my_page")
    else:
        form = PostForm()
    return render(request, POST_DIR + "post_create.html", {"form": form})


@login_required
def edit_post(request, post_id):
    """投稿を編集"""
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm(instance=post)
    return render(request, POST_DIR + "post_edit.html", {"form": form})


@login_required
def delete_post(request, post_id):
    """投稿を削除"""
    # TODO：自ユーザー以外の投稿の削除を制御
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("posts")
    return render(request, POST_DIR + "confirm_delete_post.html", {"post": post})


@login_required
def like_post(request, post_id):
    """対象ポストに対して いいね する"""
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user.is_authenticated:
        if user not in post.likes.all():
            post.likes.add(user)
        else:
            post.likes.remove(user)
        post = Post.objects.get(id=post_id)
        like_count = post.likes.count()
        context = {}
        context["like_count"] = str(like_count)
        return JsonResponse(context)
    else:
        return JsonResponse({"message": "ログインしてください"}, status=401)
