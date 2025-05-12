from typing import List, Optional

from application.ports.driven.coin_repository_port import CoinRepositoryPort
from application.ports.driving.coin_service_port import CoinServicePort
from domain.coin import Coin
from domain.historical_price import HistoricalPrice
from domain.market import Market


class CoinServices(CoinServicePort):
    def __init__(self,
                 coin_repository: CoinRepositoryPort):
        self.coin_repository = coin_repository

    async def get_coins(self) -> List[Coin]:
        return await self.coin_repository.get_coins()

    async def get_coin_with_id(self, id) -> Coin:
        return await self.coin_repository.get_coin_with_id(id)

    async def get_markets_for_coin_with_id(self, id) -> List[Market]:
        return await self.coin_repository.get_markets_for_coin_with_id(id)

    async def get_historical_price_for_coin_with_id(
            self,
            id: str,
            interval: str,
            start: Optional[int] = None,
            end: Optional[int] = None
    ) -> List[HistoricalPrice]:
        return await self.coin_repository.get_historical_price_for_coin_with_id(id, interval, start, end)
