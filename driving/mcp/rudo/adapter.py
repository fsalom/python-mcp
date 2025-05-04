from infrastructure.mcp.mcp_instance import mcp_server


@mcp_server.tool(
    name="get_rudo_info",
    description="obtener información sobre la empresa Rudo",
)
async def get_rudo_info():
    return "Rudo es una empresa de 60 trabajadores destinada a crear aplicaciones móviles"
