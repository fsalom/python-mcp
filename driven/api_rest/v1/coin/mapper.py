from typing import List

from domain import market
from domain.coin import Coin
from domain.historical_price import HistoricalPrice
from domain.market import Market
from driven.api_rest.v1.coin.models import CoinDataResponse, CoinData, MarketDataResponse, HistoricalPriceData


class CoinMapper:

    @staticmethod
    def to_domains(data: CoinDataResponse) -> List[Coin]:
        return [
            Coin(id=coin.id,
                 symbol=coin.symbol,
                 name=coin.name,
                 price_usd=coin.price_usd,
                 market_cap_usd=coin.market_cap_usd)
            for coin in data.data
        ]

    @staticmethod
    def to_domain(coin: CoinData) -> Coin:
        return Coin(id=coin.id,
                    symbol=coin.symbol,
                    name=coin.name,
                    price_usd=coin.price_usd,
                    market_cap_usd=coin.market_cap_usd)

    @staticmethod
    def to_domains_market(data: MarketDataResponse) -> List[Market]:
        return [
            Market(
                exchange_id=market.exchange_id,
                base_id=market.base_id,
                quote_id=market.quote_id,
                base_symbol=market.base_symbol,
                quote_symbol=market.quote_symbol,
                volume_usd_24hr=market.volume_usd_24hr,
                price_usd=market.price_usd,
                volume_percent=market.volume_percent
            )
            for market in data.data
        ]

    @staticmethod
    def to_domains_historical_price(data: HistoricalPriceData) -> List[HistoricalPrice]:
        return [
            HistoricalPrice(
                price_usd=price.price_usd,
                date=price.date
            )
            for price in data.data
        ]