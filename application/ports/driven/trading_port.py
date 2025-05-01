from abc import abstractmethod, ABC
from typing import Dict, Any, Optional, List


class TradingPort(ABC):
    @abstractmethod
    def get_account_balance(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_positions(self, instrument_type: str, instrument_id: Optional[str]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def place_limit_order(self, instrument: str, side: str, size: str, price: str, client_order_id: Optional[str], tag: Optional[str]) -> Dict[str, Any]:
        pass