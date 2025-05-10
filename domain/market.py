from pydantic import BaseModel


class Market(BaseModel):
    exchange_id: str
    base_id: str
    quote_id: str
    base_symbol: str
    quote_symbol: str
    volume_usd_24hr: float
    price_usd: float
    volume_percent: float
