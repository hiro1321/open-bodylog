from django.utils import timezone
import json
from ..models import Exercise, Workout, BodyWeight
from ..objects.line_config import LineConfig, Data, DataSet
from typing import List
from datetime import datetime, timedelta
from . import utils_service as utils


def create_chart_config(user: any):
    """チャート用のjsonを作成"""
    exercises = Exercise.objects.all()
    exists_exercises = [e for e in exercises if _check_workout_exists(e, user)]

    line_config = LineConfig()

    data = Data()
    week_dates = utils.get_week_dates()
    data.labels = get_labels(week_dates)

    data_sets = []
    #  TODO:body_weightレコードが存在しない場合を考慮
    data_sets.append(_get_bodyweight_dataset(user=user, target_dates=week_dates))
    for e in exists_exercises:
        dataset = _get_dataset(user, e, week_dates)
        data_sets.append(dataset)
    data.datasets = data_sets

    line_config.data = data

    line_config_dict = convert_to_dict(line_config)
    line_config_json = json.dumps(line_config_dict)

    return line_config_json


def _check_workout_exists(e: Exercise, user: any) -> bool:
    """userに対象トレーニング種目の記録が存在するかチェック"""
    workout_count = Workout.objects.filter(exercise=e, user=user).count()
    if workout_count > 0:
        return True
    else:
        return False


def get_labels(target_dates: List[datetime]) -> List[str]:
    """対象日付をラベルの形式(y/m)に変換"""
    return [dt.strftime("%-m/%-d") for dt in target_dates]


def _get_bodyweight_dataset(user: any, target_dates: List[datetime]):
    """チャート作成用のデータセットを取得(体重)"""
    data_set = DataSet()
    data_set.label = "体重"
    data_set.data = [_get_target_body_weight(user, dt) for dt in target_dates]
    data_set.borderColor = utils.generate_random_color()
    return data_set


def _get_target_body_weight(user: any, dt: datetime) -> int:
    """
    対象日付の体重を取得
    対象日付のレコードが存在しない場合、対象日付以前の一番近い日付のレコードを取得
    """
    date = dt.date()
    body_weight = (
        BodyWeight.objects.filter(user=user, date__lte=date).order_by("-date").first()
    )
    if not body_weight:
        return 0

    return str(body_weight.body_weight)


def _get_dataset(user: any, e: Exercise, target_dates: List[datetime]):
    """チャート作成用のデータセットを取得(Exerciseごと)"""
    data_set = DataSet()
    data_set.label = e.name
    data_set.data = [_get_target_exercise_weight(user, e, dt) for dt in target_dates]
    data_set.borderColor = utils.generate_random_color()
    return data_set


def _get_target_exercise_weight(user: any, e: Exercise, dt: datetime) -> int:
    """
    対象トレーニングの重量を取得
    対象日付のレコードが存在しない場合、対象日付以前の一番近い日付のレコードを取得
    """
    date = dt.date()
    workout = (
        Workout.objects.filter(user=user, exercise=e, date__lte=date)
        .order_by("-date")
        .first()
    )
    if not workout:
        return 0

    return workout.weight


def convert_to_dict(obj):
    """オブジェクトを辞書型に変換"""
    if isinstance(obj, (int, str, float)):
        return obj
    elif isinstance(obj, list):
        return [convert_to_dict(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        return {
            k: convert_to_dict(v)
            for k, v in obj.__dict__.items()
            if not callable(v) and not k.startswith("__")
        }
    else:
        return obj
