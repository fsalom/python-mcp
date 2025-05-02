from typing import List

from pydantic import BaseModel


class CoinData(BaseModel):
    id: str
    symbol: str
    name: str
    price_usd: float
    market_cap_usd: float
    change_percent_24hr: float

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
