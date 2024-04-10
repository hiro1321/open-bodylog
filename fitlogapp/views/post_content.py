from django.shortcuts import render, redirect, get_object_or_404
from ..models import Post
from ..forms import PostForm


def posts(request):
    posts = Post.objects.order_by("-created_at")
    return render(request, "fitlogapp/post_content/posts.html", {"posts": posts})


def add_post(request):
    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect("posts")
    else:
        form = PostForm()
    return render(request, "fitlogapp/post_content/add_post.html", {"form": form})


def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm(instance=post)
    return render(request, "fitlogapp/post_content/edit_post.html", {"form": form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("posts")
    return render(
        request, "fitlogapp/post_content/confirm_delete_post.html", {"post": post}
    )
