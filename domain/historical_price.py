from pydantic import BaseModel


class HistoricalPrice(BaseModel):
    price_usd: float
    date: str
