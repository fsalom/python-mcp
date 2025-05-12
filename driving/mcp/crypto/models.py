from typing import Optional

from pydantic import BaseModel


class CoinIdRequest(BaseModel):
    id: str


class HistoricalPriceRequest(BaseModel):
    id: str
    interval: str
    start: Optional[int] = None
    end: Optional[int] = None
