import asyncio
import os

from dotenv import load_dotenv
from agents import Agent, Runner

# Load variables from .env
load_dotenv()

# Verify the key exists WITHOUT displaying it
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY was not found.")

agent = Agent(
    name="Network Engineer Assistant",

    instructions="""
    You are an AI assistant for a network engineer.

    Help the user understand:
    - TCP/IP
    - BGP
    - OSPF
    - IS-IS
    - VLANs
    - MPLS
    - Cisco
    - Juniper
    - Arista
    - Azure Networking
    - Python network automation

    Explain technical concepts clearly and provide examples
    when useful.
    """,
)


async def main():
    question = input("Ask the AI agent: ")

    result = await Runner.run(
        agent,
        question,
    )

    print("\nAI Agent:")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())