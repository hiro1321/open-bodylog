from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Exercise, MusclePart, Workout, BodyWeight
from django.contrib import messages
from django.utils import timezone
from ..forms import BodyWeightForm


def select_exercise(request):
    muscle_parts = MusclePart.objects.all().order_by("pk")

    exercises_by_part = []
    for part in muscle_parts:
        exercises = Exercise.objects.filter(muscle_part=part)
        if len(exercises) == 0:
            continue
        exercises_by_part.append({"part": part, "exercises": exercises})

    return render(
        request,
        "fitlogapp/record/select_exercise.html",
        {"exercises_by_part": exercises_by_part},
    )


def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    context = {"exercise": exercise}
    return render(request, "fitlogapp/record/exercise_detail.html", context)


@login_required
def add_workout(request, exercise_id):
    exercise = Exercise.objects.get(pk=exercise_id)
    if request.method == "POST":

        user = request.user
        weight = request.POST.get("weight")
        reps = request.POST.get("reps")
        date = timezone.now().date()

        workout = Workout.objects.create(
            user=user, exercise=exercise, weight=weight, reps=reps, date=date
        )

        messages.success(request, "トレーニング記録が追加されました！")

    context = {"exercise": exercise}
    return render(request, "fitlogapp/record/exercise_detail.html", context)


@login_required
def record_bodyweight(request):
    if request.method == "POST":

        user = request.user
        weight = request.POST.get("weight")
        date = timezone.now().date()

        workout = BodyWeight.objects.create(user=user, body_weight=weight, date=date)

        messages.success(request, "記録が追加されました！")

    return render(request, "fitlogapp/record/bodyweight_detail.html")


def bodyweights(request):
    user = request.user
    # TODO:抽出条件を変更_対象userのみ_日付順で昇順
    bodyweights = BodyWeight.objects.all()
    context = {"bodyweights": bodyweights}

    return render(request, "fitlogapp/record/bodyweights.html", context)


def edit_bodyweight(request, bodyweight_id):
    bodyweight = get_object_or_404(BodyWeight, pk=bodyweight_id)

    if request.method == "POST":
        form = BodyWeightForm(request.POST, instance=bodyweight)
        if form.is_valid():
            form.save()
            return redirect("bodyweights")
    else:
        form = BodyWeightForm(instance=bodyweight)

    context = {"form": form}
    return render(request, "fitlogapp/record/bodyweight_edit.html", context)


def delete_bodyweight(request, bodyweight_id):
    bodyweight = get_object_or_404(BodyWeight, pk=bodyweight_id)

    if request.method == "POST":
        bodyweight.delete()
        return redirect("bodyweights")


def add_bodyweight(request):
    if request.method == "POST":
        form = BodyWeightForm(request.POST)
        if form.is_valid():
            bodyweight = form.save(commit=False)
            bodyweight.user = request.user
            bodyweight.save()
            return redirect("bodyweights")
    else:
        form = BodyWeightForm()

    return render(request, "fitlogapp/record/bodyweight_add.html", {"form": form})
