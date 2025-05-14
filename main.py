import sys
import os
import traceback

from driving.api_rest.router import add_routers
from infrastructure.di.app.container import AppContainer
from fastapi import FastAPI

container = AppContainer()
container.wire(modules=["driving.api_rest.v1.ai.adapter"])

app = FastAPI(title="MCP API")
add_routers(app)

# Detectar el modo de ejecución
RUN_MODE = os.environ.get("RUN_MODE", "HTTP").upper()

if RUN_MODE == "MCP":
    # Modo MCP - para usar con el protocolo MCP
    try:
        print("Inicializando en modo MCP...", file=sys.stderr)
        from fastmcp import FastMCP

        from driving.mcp.crypto.adapter import (get_crypto_coins_list, get_crypto_coin_by_id,
                                                get_markets_for_crypto_coin_with_id,
                                                get_historical_price_for_crypto_coin_with_id)
        from driving.mcp.rudo.adapter import get_rudo_info
        from driving.mcp.rick_and_morty.adapter import get_rick_and_morty_characters

        mcp_server = FastMCP.from_fastapi(app)

        mcp_server.add_tool(get_crypto_coins_list)
        mcp_server.add_tool(get_crypto_coin_by_id)
        mcp_server.add_tool(get_markets_for_crypto_coin_with_id)
        mcp_server.add_tool(get_historical_price_for_crypto_coin_with_id)
        mcp_server.add_tool(get_rudo_info)
        mcp_server.add_tool(get_rick_and_morty_characters)

        if __name__ == "__main__":
            print("Ejecutando servidor MCP...", file=sys.stderr)
            mcp_server.run()
    except Exception as e:
        print(f"Error en modo MCP: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

