from functools import cached_property

import numpy as np
import pandas as pd

from .constants import TRADING_DAYS_OF_A_YEAR
from .models import PriceHistory


class Analysis:
    DAILY_RETURN = "daily_rtn"
    ST_RETURN = "st_rtn"

    def __init__(self, history: PriceHistory):
        super().__init__()
        self._history = history

    @cached_property
    def df(self) -> pd.DataFrame:
        _df = self._history.to_df()
        _df[self.DAILY_RETURN] = _df.adjclose.pct_change()  # with daily return
        _df[self.ST_RETURN] = (
            1 + _df[self.DAILY_RETURN]
        ).cumprod()  # with st return
        return _df

    def cagr(self) -> float:
        """
        Compound Annual Growth Rate
        """
        return (
            self.df.iloc[-1][self.ST_RETURN]
            ** (TRADING_DAYS_OF_A_YEAR / len(self.df.index))
            - 1
        )

    def vol(self):
        """
        Volatility
        """
        return np.std(self.df[self.DAILY_RETURN]) * np.sqrt(
            TRADING_DAYS_OF_A_YEAR
        )

    def sharp(self):
        """
        Ex-post Sharpe ratio
        """
        return (
            np.mean(self.df[self.DAILY_RETURN])
            / np.std(self.df[self.DAILY_RETURN])
            * np.sqrt(TRADING_DAYS_OF_A_YEAR)
        )

    def mdd(self) -> float:
        return self._historical_mdd().min()

    def _historical_mdd(self) -> pd.DataFrame:
        """
        Maximum Draw Down
        """
        historical_max = self.df.adjclose.cummax()
        daily_drawdown = self.df.adjclose / historical_max - 1
        return daily_drawdown.cummin()
