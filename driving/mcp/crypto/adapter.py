from application.services.coin_service import CoinServices
from driven.api_rest.v1.coin.adapter import CoinRepositoryAdapter
from driven.api_rest.v1.coin.mapper import CoinMapper
from driving.mcp.crypto.models import CoinIdRequest
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
