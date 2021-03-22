import datetime
import enum
from dataclasses import dataclass
from typing import List

import pandas as pd

from .utils import str_to_date


class Currency(enum.Enum):
    USD = "USD"
    KRW = "KRW"


@dataclass
class Price:
    adjclose: float
    close: float
    date: datetime.date
    high: float
    low: float
    open: float
    volume: int


@dataclass
class PriceHistory:
    prices: List[Price]
    currency: Currency

    @classmethod
    def of(cls, prices: List[dict], currency: Currency):
        return cls(
            currency=currency,
            prices=[
                Price(
                    adjclose=price["adjclose"],
                    close=price["close"],
                    date=str_to_date(price["formatted_date"]),
                    high=price["high"],
                    low=price["low"],
                    open=price["open"],
                    volume=price["volume"],
                )
                for price in prices
            ],
        )

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.prices)
        return df.set_index("date")
