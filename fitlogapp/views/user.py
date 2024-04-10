from django.shortcuts import render, get_object_or_404, redirect
from ..services import chart_service
from ..models import Workout
from ..forms import WorkoutForm


def show_chart(request):
    user = request.user
    line_config_json = chart_service.create_chart_config(user)

    return render(
        request, "fitlogapp/user/workout_chart.html", {"line_config": line_config_json}
    )


def workouts(request):
    user = request.user
    # TODO:抽出条件を変更_対象userのみ_日付順で昇順
    workouts = Workout.objects.all()
    print(len(workouts))
    context = {"workouts": workouts}

    return render(request, "fitlogapp/user/workouts.html", context)


def edit_workout(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect("workouts")
    else:
        form = WorkoutForm(instance=workout)

    context = {"form": form}
    return render(request, "fitlogapp/user/edit_workout.html", context)


def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)

    if request.method == "POST":
        workout.delete()
        return redirect("workouts")


def add_workout(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect("workouts")
    else:
        form = WorkoutForm()

    return render(request, "fitlogapp/user/add_workout.html", {"form": form})
