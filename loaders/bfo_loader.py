import asyncio
from urllib import parse as urlparse
from loaders.base_loader import BaseLoader, BaseAPI


class BFOLoader(BaseLoader):
    @staticmethod
    async def get(*, name: str, train=True, **kwargs) -> dict[str, int | float | str]:
        def extract(data, keys):
            return {k: (data or {}).get(v) for k, v in keys.items()}

        api = BFOAPI()
        search_res = await api.search(name)
        company = search_res['content'][0]
        index = company['id']
        bfo_data = await api.get_bfo(index)
        bfo_data = sorted(bfo_data, key=lambda x: int(x['period']))
        period_id = bfo_data[-1]['id']
        details = await api.get_details(period_id)
        assert len(details) == 1
        details_last = details[0]

        balance_keys = {
            'intangible_assets': 'current1110',
            'fixes_assets': 'current1150',
            'non_current_assets': 'current1100',
            'reserves': 'current1210',
            'balance': 'current1600',
            'capital_and_reserves_total': 'current1300',
            'additional_capital': 'current1350',
            'long_term_liabilities': 'current1400',
            'short_term_liabilities': 'current1700',
        }
        fin_keys = {
            'revenue': 'current2110',
            'cost_price': 'current2120',
            'gross_profit': 'current2100',
            'clear_profit': 'current2400',
        }
        move_keys = {
            'income': 'current4110',
            'income_sell': 'current4111',
            'payments': 'current4120',
            'balance_stream': 'current4100',
            'income_invest': 'current4210',
            'payments_invest': 'current4220',
            'balance_invest': 'current4200',
            'income_fin': 'current4310',
            'payments_fin': 'current4320',
            'balance_fin': 'current4300',
        }
        b1 = extract(details_last.get('balance'), balance_keys)
        b2 = extract(details_last.get('financialResult'), fin_keys)
        b3 = extract(details_last.get('fundsMovement'), move_keys)
        b4 = extract(company.get('okved2'), dict(c_cat='id'))
        b5 = extract(company.get('okopf'), dict(c_type='id'))
        res = b1 | b2 | b3 | b4 | b5
        if train is False:
            res['short_name'] = company['shortName']
        return res

class BFOAPI(BaseAPI):
    headers = dict()
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    headers["Accept-Language"] = "ru,en;q=0.9"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Connection"] = "keep-alive"
    headers["Host"] = "bo.nalog.ru"
    headers["Referer"] = "https://bo.nalog.ru/organizations-card/10230627"
    headers["Sec-Fetch-Dest"] = "document"
    headers["Sec-Fetch-Mode"] = "navigate"
    headers["Sec-Fetch-Site"] = "same-origin"
    headers["Sec-Fetch-User"] = "?1"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                            "Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36"
    headers["sec-ch-ua"] = '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"'
    headers["sec-ch-ua-mobile"] = "?0"
    headers["sec-ch-ua-platform"] = '"Windows"'
    headers["Upgrade-Insecure-Requests"] = "1"

    @staticmethod
    async def search(query: str, page=0) -> dict:
        request_data = {
            'query': query,
            'page': page,
        }
        return await BFOAPI._request(
            'GET',
            'https://bo.nalog.ru/nbo/organizations/search',
            params=request_data,
            headers=BFOAPI.headers,
        )

    @staticmethod
    async def get_first_id(query: str) -> int:
        items = await BFOAPI.search(query)
        return items['content'][0]['id']

    @staticmethod
    async def get_bfo(index: int) -> dict:
        return await BFOAPI._request(
            'GET',
            f'https://bo.nalog.ru/nbo/organizations/{index}/bfo',
            headers=BFOAPI.headers,
        )

    @staticmethod
    async def get_details(bfo_index: int) -> dict:
        return await BFOAPI._request(
            'GET',
            f'https://bo.nalog.ru/nbo/bfo/{bfo_index}/details',
            headers=BFOAPI.headers,
        )

    @staticmethod
    async def get_info(index: int) -> dict:
        return await BFOAPI._request(
            'GET',
            f'https://bo.nalog.ru/nbo/organizations/{index}',
            headers=BFOAPI.headers,
        )
