from django.utils import timezone
from typing import List
from datetime import datetime, timedelta
import random


def get_week_dates() -> List[datetime]:
    """
    前1週間分のdatetimeのリストを取得(昇順)
    """
    current_date = timezone.now()
    week_dates = []

    for i in range(7):
        delta = timedelta(days=i)
        past_date = current_date - delta
        week_dates.append(past_date)

    return sorted(week_dates)


def generate_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    color_code = "#{:02x}{:02x}{:02x}".format(red, green, blue)

    return color_code
