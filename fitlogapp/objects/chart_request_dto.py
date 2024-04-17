from ..models import CustomUser, Profile
from dataclasses import dataclass


@dataclass
class ChartRequestDto:
    """
    チャート表示の画面からのリクエスト
    初期値：期間=週次, セット数=max(1回*1セット)
    """

    user_id: str = None
    period: str = "week"
    set_value: str = "max"
    rep_input: str = "1"
    set_input: str = "1"
