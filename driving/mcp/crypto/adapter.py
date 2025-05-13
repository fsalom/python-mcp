from typing import List

from application.services.coin_service import CoinServices
from domain.historical_price import HistoricalPrice
from domain.market import Market
from driven.api_rest.v1.coin.adapter import CoinRepositoryAdapter
from driven.api_rest.v1.coin.mapper import CoinMapper
from driving.mcp.crypto.models import CoinIdRequest, HistoricalPriceRequest
from infrastructure.mcp.mcp_instance import mcp_server


@mcp_server.tool(
    name="get_crypto_coins_list",
    description="get information of top 100 cryptocurrencies",
)
async def get_crypto_coins_list():
    service = CoinServices(CoinRepositoryAdapter(CoinMapper()))
    return await service.coin_repository.get_coins()


@mcp_server.tool(
    name="get_crypto_coin_by_id",
    description="Retrieve information for a specific cryptocurrency by its ID"
)
async def get_crypto_coin_by_id(request: CoinIdRequest):
    service = CoinServices(CoinRepositoryAdapter(CoinMapper()))
    return await service.coin_repository.get_coin_with_id(request.id)


@mcp_server.tool(
    name="get_markets_for_crypto_coin_with_id",
    description="Retrieve information about pricing of a specific cryptocurrency in different exchanges"
)
async def get_markets_for_crypto_coin_with_id(request: CoinIdRequest) -> List[Market]:
    service = CoinServices(CoinRepositoryAdapter(CoinMapper()))
    return await service.get_markets_for_coin_with_id(request.id)


@mcp_server.tool(
    name="get_historical_price_for_crypto_coin_with_id",
    description="Retrieve historical data for a specific asset."
                "Id (string): The slug of the asset"
                "Interval (string): interval choices m1 m5 m15 m30 h1 h2 h6 h12 d1"
                "Start (int): NIX time in milliseconds. Omitting will return the most recent asset history."
                "If start is supplied, end is required and vice versa"
                "End (int): The end timestamp for the historical data."
)
async def get_historical_price_for_crypto_coin_with_id(request: HistoricalPriceRequest) -> List[HistoricalPrice]:
    service = CoinServices(CoinRepositoryAdapter(CoinMapper()))
    return await service.get_historical_price_for_coin_with_id(request.id, request.interval, request.start, request.end)
