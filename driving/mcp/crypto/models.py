from pydantic import BaseModel


class CoinIdRequest(BaseModel):
    id: str
