import aiohttp
import base64
from solana.transaction import Transaction
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from config import JUPITER_SLIPPAGE_BPS, RPC_URL

SOL_MINT = "So11111111111111111111111111111111111111112"


async def jupiter_swap(amount_sol, user_pub, mint, sell=False):
    input_mint = mint if sell else SOL_MINT
    output_mint = SOL_MINT if sell else mint

    async with aiohttp.ClientSession() as s:
        q = await s.get(
            f"https://quote-api.jup.ag/v6/quote?inputMint={input_mint}"
            f"&outputMint={output_mint}&amount={int(amount_sol*1e9)}"
            f"&slippageBps={JUPITER_SLIPPAGE_BPS}"
        )
        quote = await q.json()
        if "data" not in quote:
            return None

        swap = await s.post(
            "https://quote-api.jup.ag/v6/swap",
            json={
                "quoteResponse": quote["data"][0],
                "userPublicKey": user_pub,
                "wrapAndUnwrapSol": True,
            },
        )
        data = await swap.json()
        return data["swapTransaction"]


async def send_swap(tx_base64, secret):
    client = AsyncClient(RPC_URL)

    tx_bytes = base64.b64decode(tx_base64)
    tx = Transaction.deserialize(tx_bytes)

    kp = Keypair.from_bytes(base64.b64decode(secret))

    tx.sign(kp)
    await client.send_transaction(tx)
    await client.close()
