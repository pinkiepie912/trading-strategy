from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass
from typing import List

from yahoofinancials import YahooFinancials

from ..constants import DATE_FMT
from .exceptions import InvalidTickerError, NoHistoricalDataError


class Interval(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# TODO: 개발 편의상 client를 두었으나, trading repo로 이전해야함.
class YahooFinanceClient:
    def __init__(self):
        # TODO: if necessary, add context
        super().__init__()

    def get_historical_data(
        self,
        ticker: str,
        start_date: datetime.date,
        end_date: datetime.date,
        time_interval: Interval,
    ) -> List[Price]:
        yahoo_financial = YahooFinancials(ticker)
        history = yahoo_financial.get_historical_price_data(
            start_date=self._date_to_str(start_date),
            end_date=self._date_to_str(end_date),
            time_interval=time_interval.value,
        )

        if "price" not in history[ticker]:
            raise InvalidTickerError

        prices = history[ticker]["price"]
        if not prices:
            raise NoHistoricalDataError

        return [
            Price(
                adjclose=price["adjclose"],
                close=price["close"],
                date=self._str_to_date(price["formatted_date"]),
                high=price["high"],
                low=price["low"],
                open=price["open"],
                volume=price["volume"],
            )
            for price in prices
        ]

    def _date_to_str(self, date: datetime.date, fmt=DATE_FMT) -> str:
        return date.strftime(fmt)

    def _str_to_date(self, str_date: str, fmt=DATE_FMT) -> datetime.date:
        return datetime.datetime.strptime(str_date, fmt).date()


@dataclass
class Price:
    adjclose: float
    close: float
    date: datetime.date
    high: float
    low: float
    open: float
    volume: int
