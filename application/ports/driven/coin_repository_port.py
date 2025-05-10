from abc import abstractmethod, ABC
from typing import List
from domain.coin import Coin
from domain.market import Market


class CoinRepositoryPort(ABC):
    @abstractmethod
    def get_coins(self) -> List[Coin]:
        pass

    @abstractmethod
    def get_coin_with_id(self, id) -> Coin:
        pass

    @abstractmethod
    def get_markets_for_coin_with_id(self, id) -> List[Market]:
        pass
