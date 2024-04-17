from django.utils import timezone
from typing import List
from datetime import datetime, timedelta
import random


def get_target_period_dates(period_date: int, step: int) -> List[datetime]:
    """
    対象期間のdatetimeのリストを取得(昇順)
    Args:
        period(int): 対象範囲
        step(int): 日付の感覚
    Returns:
        List[datetime]: 対象期間の日付のリスト
    """
    current_date = timezone.now()
    target_date = []
    for i in range(0, period_date, step):
        delta = timedelta(days=i)
        past_date = current_date - delta
        target_date.append(past_date)

    return sorted(target_date)


def generate_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    color_code = "#{:02x}{:02x}{:02x}".format(red, green, blue)

    return color_code
