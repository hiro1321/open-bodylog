from django import forms
from .models import Workout, Profile, Post, BodyWeight


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["exercise", "date", "reps", "weight"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image", "bio"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]


class BodyWeightForm(forms.ModelForm):
    class Meta:
        model = BodyWeight
        fields = ["date", "body_weight"]
