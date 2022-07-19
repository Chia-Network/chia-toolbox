from typing import List, Optional

import aiohttp


from chia.cmds.wallet_funcs import get_wallet
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.types.blockchain_format.sized_bytes import bytes32

from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.config import load_config
from chia.util.ints import uint16, uint64
from chia.wallet.trade_record import TradeRecord
from chia.wallet.trading.offer import Offer


async def get_client(wallet_rpc_port: Optional[int], fingerprint: int) -> Optional[WalletRpcClient]:
    try:
        config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
        self_hostname = config["self_hostname"]
        if wallet_rpc_port is None:
            wallet_rpc_port = config["wallet"]["rpc_port"]
        wallet_client = await WalletRpcClient.create(self_hostname, uint16(wallet_rpc_port), DEFAULT_ROOT_PATH, config)
        wallet_client_f = await get_wallet(wallet_client, fingerprint=fingerprint)
        if wallet_client_f is None:
            wallet_client.close()
            await wallet_client.await_closed()
            return None
        wallet_client, fingerprint = wallet_client_f
        return  wallet_client
    except KeyboardInterrupt:
        pass
    except Exception as e:
        if isinstance(e, aiohttp.ClientConnectorError):
            print(
                f"Connection error. Check if the wallet is running at {wallet_rpc_port}. "
                "You can run the wallet via:\n\tchia start wallet"
            )
        else:
            print(f"Exception from 'wallet' {e}")
    wallet_client.close()
    await wallet_client.await_closed()


async def select_offers(asset_id: str, cancel_all: bool, wallet_rpc_port: Optional[int], fingerprint: int) -> List[bytes32]:
    wallet_client = await get_client(wallet_rpc_port, fingerprint)
    batch_size: int = 10
    start: int = 0
    end: int = start + batch_size
    records: List[bytes32] = []
    # Traverse offers page by page
    while True:
        trades: List[TradeRecord] = await wallet_client.get_all_offers(
            start,
            end,
            file_contents=True,
            reverse=True,
            exclude_my_offers=False,
            exclude_taken_offers=True,
            include_completed=False,
        )
        for trade in trades:
            if cancel_all:
                records.append(trade.trade_id)
                continue
            if trade.offer and trade.offer != b'':
                summary = Offer.from_bytes(trade.offer).summary()
                if asset_id == list(summary[0].keys())[0]:
                    records.append(trade.trade_id)
                    continue

                if asset_id == list(summary[1].keys())[0]:
                    records.append(trade.trade_id)
                    continue

        if len(trades) < batch_size:
            break

        start = end
        end += batch_size
    return records


async def cancel_offers(asset_id: str, cancel_all: bool, wallet_rpc_port: Optional[int], fingerprint: int, fee: int, dry_run: bool):
    trades = await select_offers(asset_id, cancel_all, wallet_rpc_port, fingerprint)
    print(f"Found {len(trades)} offers about {asset_id} need to cancel ...")
    wallet_client = await get_client(wallet_rpc_port, fingerprint)
    count = 0
    for tid in trades:
        print(f"Cancelling offer {tid}, {count} out of {len(trades)} ...")
        if not dry_run:
            await wallet_client.cancel_offer(tid, uint64(fee), True)
        count += 1
    print(f"Cancelled {len(trades)} offers.")