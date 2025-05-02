import os
from typing import List

import httpx
from application.ports.driven.coin_repository_port import CoinRepositoryPort
from domain.coin import Coin
from driven.api_rest.v1.coin.mapper import CoinMapper
from driven.api_rest.v1.coin.models import CoinDataResponse


class CoinRepositoryAdapter(CoinRepositoryPort):
    def __init__(self, mapper: CoinMapper):
        self.mapper = mapper

    async def get_coins(self) -> List[Coin]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://rest.coincap.io/v3/assets?apiKey={os.getenv('API_KEY')}")
            response.raise_for_status()

            data = CoinDataResponse(**response.json())
            return self.mapper.to_domains(data)
