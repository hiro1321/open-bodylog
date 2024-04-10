from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from ..models import Profile
from ..forms import ProfileForm


def view_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(
        request, "fitlogapp/profile/view_profile.html", {"profile": user_profile}
    )


def edit_profile(request):
    user_profile = Profile.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("profile")
    else:
        if user_profile:
            form = ProfileForm(instance=user_profile)
        else:
            form = ProfileForm()

    return render(request, "fitlogapp/profile/edit_profile.html", {"form": form})
