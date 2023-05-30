import logging
from abc import ABC, abstractmethod

import aiohttp


class BaseLoader(ABC):
    @staticmethod
    @abstractmethod
    async def get(*, name: str, train=True, **kwargs) -> dict[str, int | float | str]:
        pass


class BaseAPI(ABC):
    @staticmethod
    async def _request(req_type: str, url: str, **kwargs) -> dict:
        async with aiohttp.ClientSession() as session:
            match req_type:
                case 'GET':
                    method = session.get
                case 'POST':
                    method = session.post
                case _:
                    raise Exception
            async with method(url, **kwargs) as response:
                try:
                    json = await response.json()
                except Exception:
                    logging.error(await response.text())
                    raise

                return json
