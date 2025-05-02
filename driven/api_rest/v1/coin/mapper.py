from typing import List

from domain.coin import Coin
from driven.api_rest.v1.coin.models import CoinDataResponse


class CoinMapper:

    @staticmethod
    def to_domains(data: CoinDataResponse) -> List[Coin]:
        return [
            Coin(
                id=coin.id,
                symbol=coin.symbol,
                name=coin.name,
                price_usd=coin.price_usd,
                market_cap_usd=coin.market_cap_usd,
            )
            for coin in data.data
        ]
