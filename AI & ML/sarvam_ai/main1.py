import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="uvx",
        args=["sarvam-mcp"],
        env={
            "SARVAM_API_KEY": "sk_4sw4a2u6_BUoGULkGt69Fh89sqJRN4Xvg"
        }
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("\nConnected to Sarvam MCP\n")

            tools = await session.list_tools()

            for tool in tools.tools:

                print("=" * 70)

                print("TOOL:")
                print(tool.name)

                print("\nDESCRIPTION:")
                print(tool.description)

                print("\nINPUT SCHEMA:")

                print(
                    json.dumps(
                        tool.inputSchema,
                        indent=4
                    )
                )


asyncio.run(main())