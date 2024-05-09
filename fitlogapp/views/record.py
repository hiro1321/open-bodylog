from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Exercise, MusclePart, Workout, BodyWeight
from django.contrib import messages
from django.utils import timezone
from ..forms import BodyWeightForm, WorkoutForm


RECORD_DIR = "fitlogapp/record/"


@login_required
def record_bodyweight(request):
    """体重登録のview"""
    # TODO:前回の記録を登録できるようにする
    # TODO:スライドバーの上限値前回記録の+10%までにする
    if request.method == "POST":
        user = request.user
        weight = request.POST.get("weight")
        date = timezone.now().date()
        BodyWeight.objects.create(user=user, body_weight=weight, date=date)
        messages.success(request, "記録が追加されました！")

    return render(request, RECORD_DIR + "bodyweight_detail.html")


@login_required
def bodyweights(request):
    """ログインユーザーの体重記録一覧を表示"""
    user = request.user
    # TODO:抽出条件を変更_対象userのみ_日付順で昇順
    bodyweights = BodyWeight.objects.filter(user=user).order_by("-date")
    context = {"bodyweights": bodyweights}

    return render(request, RECORD_DIR + "bodyweights.html", context)


@login_required
def add_bodyweight(request):
    """体重記録の追加"""
    if request.method == "POST":
        form = BodyWeightForm(request.POST)
        if form.is_valid():
            bodyweight = form.save(commit=False)
            bodyweight.user = request.user
            bodyweight.save()
            return redirect("bodyweights")
    else:
        form = BodyWeightForm()

    return render(request, RECORD_DIR + "bodyweight_add.html", {"form": form})


@login_required
def edit_bodyweight(request, bodyweight_id):
    """体重記録の修正"""
    # TODO:追加と同じhtmlコンポーネントを使う
    # TODO:成功時のメッセージを返す
    bodyweight = get_object_or_404(BodyWeight, pk=bodyweight_id)
    if request.method == "POST":
        form = BodyWeightForm(request.POST, instance=bodyweight)
        if form.is_valid():
            form.save()
            return redirect("bodyweights")
    else:
        form = BodyWeightForm(instance=bodyweight)

    context = {"form": form}
    return render(request, RECORD_DIR + "bodyweight_edit.html", context)


@login_required
def delete_bodyweight(request, bodyweight_id):
    """体重記録の削除"""
    # TODO:想定外データのハンドリング
    bodyweight = get_object_or_404(BodyWeight, pk=bodyweight_id)

    if request.method == "POST":
        bodyweight.delete()
        return redirect("bodyweights")


@login_required
def select_exercise(request):
    """トレーニング記録の追加(種目を選択)"""
    muscle_parts = MusclePart.objects.all().order_by("pk")

    exercises_by_part = []
    for part in muscle_parts:
        exercises = Exercise.objects.filter(muscle_part=part)
        if len(exercises) == 0:
            continue
        exercises_by_part.append({"part": part, "exercises": exercises})

    return render(
        request,
        RECORD_DIR + "select_exercise.html",
        {"exercises_by_part": exercises_by_part},
    )


def exercise_detail(request, exercise_id):
    """トレーニング記録の追加(詳細)"""
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    context = {"exercise": exercise}
    return render(request, RECORD_DIR + "workout_detail.html", context)


@login_required
def submit_workout(request, exercise_id):
    """トレーニング記録の追加(詳細画面から)"""
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
    return render(request, RECORD_DIR + "workout_detail.html", context)


@login_required
def workouts(request):
    """対象ユーザーのトレーニング記録の一覧を表示"""
    user = request.user
    # TODO:抽出条件を変更_対象userのみ_日付順で昇順
    workouts = Workout.objects.all().filter(user=user).order_by("-date")
    print(len(workouts))
    context = {"workouts": workouts}

    return render(request, RECORD_DIR + "workouts.html", context)


@login_required
def add_workout(request):
    """トレーニング記録を追加(編集画面から)"""
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect("workouts")
    else:
        form = WorkoutForm()

    return render(request, RECORD_DIR + "workout_add.html", {"form": form})


@login_required
def edit_workout(request, workout_id):
    """トレーニング記録を編集"""
    workout = get_object_or_404(Workout, pk=workout_id)

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect("workouts")
    else:
        form = WorkoutForm(instance=workout)

    context = {"form": form}
    return render(request, RECORD_DIR + "workout_edit.html", context)


@login_required
def delete_workout(request, workout_id):
    """トレーニング記録を削除"""
    workout = get_object_or_404(Workout, pk=workout_id)

    if request.method == "POST":
        workout.delete()
        return redirect("workouts")
