from django.utils import timezone
from django.db import connection

import json
from ..models import Exercise, Workout, BodyWeight, CustomUser
from ..objects.line_config import LineConfig, Data, DataSet
from ..objects.chart_request_dto import ChartRequestDto
from typing import List, Tuple
from datetime import datetime
from ..models import CustomUser
from . import utils_service as utils


def signup_validate(request):

    return


def check_email_exists(email) -> bool:
    """
    emailが登録済みか否か（メールアドレスが一致  and メール認証フラグ=True）

    Args:
        email:メールアドレス
    Returns:
        bool:ユーザー登録済みか
    """
    users = CustomUser.objects.filter(email=email, is_email_verified=True)
    return users.count() >= 1


def is_username_taken(username) -> bool:
    """
    ユーザー名が登録済みか否か

    Args:
        username:ユーザー名
    Returns:
        bool:ユーザー名が使われているか否か
    """
    return CustomUser.objects.filter(custom_username=username).exists()


# def is_username_taken(user_name) -> bool:
#     """
#     ユーザーが使用済みか否か
#     """
#     users = CustomUser.objects.filter(custom_username=user_name)
#     return users.count() >= 1


# def create_chart_config(chart_request_dto: ChartRequestDto):
#     """チャート用のjsonを作成"""
#     user = CustomUser.objects.get(id=chart_request_dto.user_id)
#     exercises = Exercise.objects.all()
#     exists_exercises = [
#         e for e in exercises if _check_workout_exists(e, chart_request_dto)
#     ]

#     line_config = LineConfig()

#     data = Data()
#     period_date, step = _get_period_date(user, chart_request_dto.period)
#     target_dates = utils.get_target_period_dates(period_date, step)
#     data.labels = _get_labels(target_dates)

#     data_sets = []
#     #  TODO:body_weightレコードが存在しない場合を考慮
#     data_sets.append(_get_bodyweight_dataset(user=user, target_dates=target_dates))
#     for e in exists_exercises:
#         dataset = _get_dataset(user, e, target_dates, chart_request_dto)
#         data_sets.append(dataset)
#     data.datasets = data_sets

#     line_config.data = data

#     line_config_dict = _convert_to_dict(line_config)
#     line_config_json = json.dumps(line_config_dict)

#     return line_config_json


# def _check_workout_exists(e: Exercise, chart_request_dto: ChartRequestDto) -> bool:
#     """userに対象トレーニング種目の記録が存在するかチェック"""
#     weight = _get_target_exercise_weight(e, chart_request_dto, datetime.now().date())
#     if weight:
#         return True
#     else:
#         return False


# def _get_target_exercise_weight(
#     e: Exercise, chart_request_dto: ChartRequestDto, date: any
# ):
#     """ """
#     set_amount = int(chart_request_dto.set_input)

#     offset = ""
#     if set_amount > 2:
#         offset = "OFFSET " + str(set_amount - 1)

#     date_str = date.strftime("%Y-%m-%d")

#     with connection.cursor() as cursor:
#         sql_query = """
#             SELECT
#               weight
#             FROM
#               fitlogapp_workout
#             WHERE
#               (user_id, exercise_id, date) IN (
#                 SELECT
#                   user_id,
#                   exercise_id,
#                   date
#                 FROM
#                   fitlogapp_workout
#                 WHERE
#                   user_id = {0}  AND
#                   exercise_id = {1} AND
#                   reps >= {2} AND
#                   date <= {3}
#                 GROUP BY
#                   user_id,
#                   exercise_id,
#                   date
#                 HAVING
#                   COUNT(*) >= {4}
#                 )
#             GROUP BY
#               id,
#               exercise_id,
#               date
#             ORDER BY
#               date DESC,
#               weight DESC
#             LIMIT 1
#               {5}
#             """.format(
#             chart_request_dto.user_id,
#             e.pk,
#             chart_request_dto.rep_input,
#             "'" + date_str + "'",
#             set_amount,
#             offset,
#         )
#         cursor.execute(sql_query)
#         rows = cursor.fetchall()
#         if rows:

#             return rows[0][0]
#         else:
#             return None


# def _get_period_date(user: any, period: str) -> Tuple[int, int]:
#     if period == "week":
#         return (7, 1)
#     elif period == "year":
#         return (365 + 1, 5)
#     elif period == "all":
#         # TODO:体重の情報が抜け落ちる
#         workout = Workout.objects.filter(user=user).order_by("date").first()
#         current_dt = timezone.now()
#         current_date = current_dt.date()
#         period_delta = current_date - workout.date
#         period_days = period_delta.days

#         # period_dateが存在しない or 0 の場合を考慮
#         step = 1
#         if period_days > 200:
#             step = round(period_days / 100)
#         return (period_days + 1, step)


# def _get_labels(target_dates: List[datetime]) -> List[str]:
#     """対象日付をラベルの形式(y/m)に変換"""
#     return [dt.strftime("%-m/%-d") for dt in target_dates]


# def _get_bodyweight_dataset(user: any, target_dates: List[datetime]):
#     """チャート作成用のデータセットを取得(体重)"""
#     data_set = DataSet()
#     data_set.label = "体重"
#     data_set.data = [_get_target_body_weight(user, dt) for dt in target_dates]
#     data_set.borderColor = utils.generate_random_color()
#     return data_set


# def _get_target_body_weight(user: any, dt: datetime) -> int:
#     """
#     対象日付の体重を取得
#     対象日付のレコードが存在しない場合、対象日付以前の一番近い日付のレコードを取得
#     """
#     date = dt.date()
#     body_weight = (
#         BodyWeight.objects.filter(user=user, date__lte=date).order_by("-date").first()
#     )
#     if not body_weight:
#         return 0

#     return str(body_weight.body_weight)


# def _get_dataset(
#     user: any,
#     e: Exercise,
#     target_dates: List[datetime],
#     chart_request_dto: ChartRequestDto,
# ):
#     """チャート作成用のデータセットを取得(Exerciseごと)"""
#     data_set = DataSet()
#     data_set.label = e.name

#     data_list = []
#     for dt in target_dates:
#         weight = _get_target_exercise_weight(e, chart_request_dto, dt.date())
#         if weight:
#             print(weight)
#             data_list.append(weight)
#         else:
#             data_list.append(0)
#     print(data_list)
#     data_set.data = data_list

#     data_set.borderColor = utils.generate_random_color()
#     return data_set


# def _convert_to_dict(obj):
#     """オブジェクトを辞書型に変換"""
#     if isinstance(obj, (int, str, float)):
#         return obj
#     elif isinstance(obj, list):
#         return [_convert_to_dict(v) for v in obj]
#     elif isinstance(obj, dict):
#         return {k: _convert_to_dict(v) for k, v in obj.items()}
#     elif hasattr(obj, "__dict__"):
#         return {
#             k: _convert_to_dict(v)
#             for k, v in obj.__dict__.items()
#             if not callable(v) and not k.startswith("__")
#         }
#     else:
#         return obj
