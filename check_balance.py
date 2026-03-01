from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
import asyncio

async def check():
    address = "CJHP4EdhyTWDwcMmZCPApYeMkq6hCfmoSxLTxM7YRytU"
    async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
        resp = await client.get_balance(Pubkey.from_string(address))
        print("SOL:", resp.value / 1e9)

asyncio.run(check())
