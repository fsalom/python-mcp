from abc import abstractmethod, ABC
from typing import List, Optional

from domain.coin import Coin
from domain.historical_price import HistoricalPrice
from domain.market import Market


class CoinServicePort(ABC):
    @abstractmethod
    def get_coins(self) -> List[Coin]:
        pass

    @abstractmethod
    def get_coin_with_id(self, id) -> Coin:
        pass

    @abstractmethod
    def get_markets_for_coin_with_id(self, id) -> List[Market]:
        pass

    @abstractmethod
    def get_historical_price_for_coin_with_id(
            self,
            id: str,
            interval: str,
            start: Optional[int] = None,
            end: Optional[int] = None
    ) -> List[HistoricalPrice]:
        pass
