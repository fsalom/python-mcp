from infrastructure.mcp.mcp_instance import mcp_server


@mcp_server.tool(
    name="get_rick_and_morty_characters",
    description="obtener listado de personajes de rick and morty",
)
async def get_rick_and_morty_characters():
    return "Morty, 14 años"