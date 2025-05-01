from typing import List

from application.ports.driven.coin_repository_port import CoinRepositoryPort
from application.ports.driving.coin_service_port import CoinServicePort
from domain.coin import Coin


class CoinServices(CoinServicePort):
    def __init__(self,
                 coin_repository: CoinRepositoryPort):
        self.coin_repository = coin_repository

    async def get_coins(self) -> List[Coin]:
        return self.coin_repository.get_coins()
