from __future__ import annotations

import datetime
import enum

from yahoofinancials import YahooFinancials

from ..models import Currency, PriceHistory
from ..utils import date_to_str
from .exceptions import (
    InvalidPeriodError,
    InvalidTickerError,
    NoHistoricalDataError,
)


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
    ) -> PriceHistory:
        if start_date > end_date:
            raise InvalidPeriodError

        yahoo_financial = YahooFinancials(ticker)
        data = yahoo_financial.get_historical_price_data(
            start_date=date_to_str(start_date),
            end_date=date_to_str(end_date),
            time_interval=time_interval.value,
        )

        data = data[ticker]
        if "prices" not in data:
            raise InvalidTickerError

        prices = data["prices"]
        if not prices:
            raise NoHistoricalDataError

        return PriceHistory.of(prices, Currency(data["currency"]))
