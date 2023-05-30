import time
from abc import ABC, abstractmethod

from pytrends import request as pt
from loaders.base_loader import BaseLoader
from time import sleep


class GoogleTrendLoader(BaseLoader):
    @staticmethod
    async def get(*, name: str, train=True, **kwargs):
        return {
            'ggl_trend5': await GoogleTrendLoader._get_trend(name, 5),
            'ggl_trend10': await GoogleTrendLoader._get_trend(name, 10),
        }

    @staticmethod
    async def _get_trend(name: str, n: int = 5):
        sleep(0.1)
        req = pt.TrendReq()
        req.build_payload([name])
        res = req.interest_over_time()
        try:
            return res[name].iloc[-n:].sum()
        except Exception:
            return 0
