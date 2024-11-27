from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import top_page as top_views
from .views import account as account_views
from .views import record as record_views
from .views import user as user_views
from .views import profile as profile_views
from .views import post as post_views

urlpatterns = [
    path("", top_views.top_page, name="top_page"),
    # ユーザー認証機能
    path("signup/", account_views.signup, name="signup"),
    path(
        "verify/<str:verification_code>/",
        account_views.verify_email,
        name="verify_email",
    ),
    path("user_register/", account_views.user_register, name="user_register"),
    path("login/", account_views.user_login, name="login"),
    path("logout/", account_views.user_logout, name="logout"),
    # 体重記録機能
    path(
        "record/record_bodyweight/",
        record_views.record_bodyweight,
        name="record_bodyweight",
    ),
    path("record/bodyweights/", record_views.bodyweights, name="bodyweights"),
    path("record/bodyweights/add/", record_views.add_bodyweight, name="add_bodyweight"),
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
    # トレーニング記録機能
    path(
        "record/select_exercise/", record_views.select_exercise, name="select_exercise"
    ),
    path(
        "record/detail/<int:exercise_id>/",
        record_views.exercise_detail,
        name="exercise_detail",
    ),
    path(
        "record/submit_workout/<int:exercise_id>/",
        record_views.submit_workout,
        name="submit_workout",
    ),
    path("record/workouts/", record_views.workouts, name="workouts"),
    path("record/workouts/add/", record_views.add_workout, name="add_workout"),
    path(
        "user/workouts/<int:workout_id>/edit/",
        record_views.edit_workout,
        name="edit_workout",
    ),
    path(
        "workouts/delete/<int:workout_id>/",
        record_views.delete_workout,
        name="delete_workout",
    ),
    # ユーザー情報表示/編集機能
    path("my_page/", user_views.my_page, name="my_page"),
    path("user/<str:custom_username>/", user_views.show_user, name="show_user"),
    path("create_chert/", user_views.create_chert, name="create_chert"),
    path("edit_profile/", user_views.edit_profile, name="edit_profile"),
    path("liked_users/<int:post_id>/", user_views.liked_users, name="liked_users"),
    # フォロー機能
    path(
        "toggle_follow/<int:user_id>/", user_views.toggle_follow, name="toggle_follow"
    ),
    path(
        "following/<int:user_id>/", user_views.following_users, name="following_users"
    ),
    path(
        "followers/<int:user_id>/", user_views.followers_users, name="followers_users"
    ),
    # 投稿機能
    path("posts/create", post_views.create_post, name="create_post"),
    path("edit/<int:post_id>/", post_views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", post_views.delete_post, name="delete_post"),
    path("like_post/<int:post_id>/", post_views.like_post, name="like_post"),
    # TODO:パスパラメータはuser_idではなくusernameに統一
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
