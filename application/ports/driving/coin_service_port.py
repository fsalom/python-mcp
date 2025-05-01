from abc import abstractmethod, ABC
from typing import List

from domain.coin import Coin


class CoinServicePort(ABC):
    @abstractmethod
    def get_coins(self) -> List[Coin]:
        pass
