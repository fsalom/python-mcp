from pydantic import BaseModel


class Coin(BaseModel):
    id: str
    symbol: str
    name: str
    price_usd: float
    market_cap_usd: float
    change_percent_24hr: float

