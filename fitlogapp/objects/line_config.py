from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class DataSet:
    label: str = None
    data: List[float] = None
    borderColor: str = None


@dataclass
class Data:
    labels: List[str] = None
    datasets: List[DataSet] = None


@dataclass
class ParamY:
    suggestedMin: int = 0
    suggestedMax: int = 150
    ticks: Dict[str, int] = field(default_factory=lambda: {"stepSize": 5})


@dataclass
class Options:
    scales: Dict[str, ParamY] = field(default_factory=lambda: {"y": ParamY()})


@dataclass
class LineConfig:
    type: str = "line"
    data: Data = None
    options: Options = field(default_factory=Options)
