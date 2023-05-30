from abc import ABC, abstractmethod

from pytrends import request as pt
from loaders.base_loader import BaseLoader
from time import sleep


def val_rent(income, profit):
    if income is None or profit is None:
        return dict(val_rent=None)
    return dict(val_rent=income / profit if profit != 0 else 0)


def roa(clear_profit, actives):
    if clear_profit is None or actives is None:
        return dict(roa=None)
    return dict(roa=clear_profit / actives if actives != 0 else 0)


def cr(cur_actives, short_term_liabilities):
    if cur_actives is None or short_term_liabilities is None:
        return dict(cr=None)
    return dict(cr=cur_actives / short_term_liabilities if short_term_liabilities != 0 else 0)


class StatLoader(BaseLoader):
    @staticmethod
    async def get(*, name: str, train=True, **kwargs):
        return val_rent(
            kwargs.get('revenue'), kwargs.get('gross_profit')
        ) | roa(
            kwargs.get('clear_profit'), kwargs.get('non_current_assets')
        ) | cr(
            kwargs.get('balance'), kwargs.get('short_term_liabilities')
        )
