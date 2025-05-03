from application.services.coin_service import CoinServices
from driven.api_rest.v1.coin.adapter import CoinRepositoryAdapter
from driven.api_rest.v1.coin.mapper import CoinMapper
from main import mcp_server


@mcp_server.tool(
    name="get_crypto_coins_list",
    description="Call api of coincap and retrieve information of top 100 cryptocurrencies",
)
async def get_crypto_coins_list():
    service = CoinServices(CoinRepositoryAdapter(CoinMapper()))
    return await service.coin_repository.get_coins()
