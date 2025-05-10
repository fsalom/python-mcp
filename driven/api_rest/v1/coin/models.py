from typing import List

from okx import MarketData
from pydantic import BaseModel, Field


class CoinData(BaseModel):
    id: str
    symbol: str
    name: str
    price_usd: float
    market_cap_usd: float

    class Config:
        alias_generator = lambda field: ''.join(
            word.capitalize() if i > 0 else word
            for i, word in enumerate(field.split('_'))
        )
        populate_by_name = True
        from_attributes = True


class CoinDataResponse(BaseModel):
    data: List[CoinData]
    timestamp: int

    class Config:
        from_attributes = True


class CoinDataSingleResponse(BaseModel):
    data: CoinData
    timestamp: int

    class Config:
        from_attributes = True


class MarketDataResponse(BaseModel):
    data: List[MarketData]
    timestamp: int


class MarketData(BaseModel):
    exchange_id: str = Field(alias="exchangeId")
    base_id: str = Field(alias="baseId")
    quote_id: str = Field(alias="quoteId")
    base_symbol: str = Field(alias="baseSymbol")
    quote_symbol: str = Field(alias="quoteSymbol")
    volume_usd_24hr: float = Field(alias="volumeUsd24Hr")
    price_usd: float = Field(alias="priceUsd")
    volume_percent: float = Field(alias="volumePercent")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        from_attributes = True


class HistoricalPriceData(BaseModel):
    price_usd: float = Field(alias="priceUsd")
    date: str


class HistoricalData(BaseModel):
    data: List[HistoricalPriceData]
    timestamp: int
