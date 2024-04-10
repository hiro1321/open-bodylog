from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import top_page as top_views
from .views import home as home_views
from .views import account as account_views
from .views import record as record_views
from .views import user as user_views
from .views import profile as profile_views
from .views import post_content as post_views

urlpatterns = [
    path("", top_views.top_page, name="top_page"),
    path("register/", account_views.register, name="register"),
    path(
        "verify/<str:verification_code>/",
        account_views.verify_email,
        name="verify_email",
    ),
    path("login/", account_views.user_login, name="login"),
    path("logout/", account_views.user_logout, name="logout"),
    # path("<str:custom_username>/", views.user_profile_view, name="user_profile"),
    path("user/home/", home_views.home_page, name="home_page"),
    path(
        "record/record_bodyweight/",
        record_views.record_bodyweight,
        name="record_bodyweight",
    ),
    path("record/bodyweights/", record_views.bodyweights, name="bodyweights"),
    path(
        "record/bodyweights/<int:bodyweight_id>/edit/",
        record_views.edit_bodyweight,
        name="edit_bodyweight",
    ),
    path(
        "record/bodyweights/delete/<int:bodyweight_id>/",
        record_views.delete_bodyweight,
        name="delete_bodyweight",
    ),
    path("record/bodyweights/add/", record_views.add_bodyweight, name="add_bodyweight"),
    path(
        "record/select_exercise/", record_views.select_exercise, name="select_exercise"
    ),
    path(
        "record/detail/<int:exercise_id>/",
        record_views.exercise_detail,
        name="exercise_detail",
    ),
    path(
        "record/add_workout/<int:exercise_id>/",
        record_views.add_workout,
        name="add_workout",
    ),
    path("user/show_chart/", user_views.show_chart, name="show_chart"),
    path("user/workouts/", user_views.workouts, name="workouts"),
    path(
        "user/workouts/<int:workout_id>/edit/",
        user_views.edit_workout,
        name="edit_workout",
    ),
    path(
        "workouts/delete/<int:workout_id>/",
        user_views.delete_workout,
        name="delete_workout",
    ),
    path("user/workouts/add/", user_views.add_workout, name="add_workout"),
    path("profile/", profile_views.view_profile, name="profile"),
    path("edit_profile/", profile_views.edit_profile, name="edit_profile"),
    path("posts/", post_views.posts, name="posts"),
    path("posts/add", post_views.add_post, name="add_post"),
    path("edit/<int:post_id>/", post_views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", post_views.delete_post, name="delete_post"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
