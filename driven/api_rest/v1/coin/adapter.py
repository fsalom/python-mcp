import os
from typing import List, Optional

import httpx
from application.ports.driven.coin_repository_port import CoinRepositoryPort
from domain.coin import Coin
from domain.historical_price import HistoricalPrice
from domain.market import Market
from driven.api_rest.v1.coin.mapper import CoinMapper
from driven.api_rest.v1.coin.models import CoinDataResponse, CoinDataSingleResponse, MarketDataResponse, \
    HistoricalPriceData, HistoricalData


class CoinRepositoryAdapter(CoinRepositoryPort):
    def __init__(self, mapper: CoinMapper):
        self.mapper = mapper

    async def get_coins(self) -> List[Coin]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://rest.coincap.io/v3/assets?apiKey={os.getenv('API_KEY')}")
            response.raise_for_status()

            data = CoinDataResponse(**response.json())
            return self.mapper.to_domains(data)

    async def get_coin_with_id(self, id) -> Coin:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://rest.coincap.io/v3/assets/{id}/?apiKey={os.getenv('API_KEY')}")
            response.raise_for_status()

            info = CoinDataSingleResponse(**response.json())
            return self.mapper.to_domain(info.data)

    async def get_markets_for_coin_with_id(self, id) -> List[Market]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://rest.coincap.io/v3/assets/{id}/markets/?apiKey={os.getenv('API_KEY')}")
            response.raise_for_status()

            info = MarketDataResponse(**response.json())
            return self.mapper.to_domains_market(info)

    async def get_historical_price_for_coin_with_id(
        self,
        id: str,
        interval: str,
        start: Optional[int] = None,
        end: Optional[int] = None
    ) -> List[HistoricalPrice]:
        url = f"https://rest.coincap.io/v3/assets/{id}/history"
        params = {
            "interval": interval,
            "apiKey": os.getenv("API_KEY")
        }

        if start:
            params["start"] = start
        if end:
            params["end"] = end

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

            info = HistoricalData(**response.json())
            return self.mapper.to_domains_historical_price(info.data)
