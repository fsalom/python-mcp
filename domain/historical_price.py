from pydantic import BaseModel


class HistoricalPrice(BaseModel):
    priceUsd: float
    date: str
