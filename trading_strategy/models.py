import datetime
import enum
from dataclasses import dataclass
from typing import List

import pandas as pd


class Currency(enum.Enum):
    USD = "USD"
    KRW = "KRW"


@dataclass
class Price:
    ticker: str
    currency: Currency
    adjclose: float
    close: float
    date: datetime.date
    high: float
    low: float
    open: float
    volume: int


@dataclass
class PriceHistory:
    name: str
    ticker: str
    currency: Currency
    prices: List[Price]

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.prices)
        df.set_index("date")
        return df
