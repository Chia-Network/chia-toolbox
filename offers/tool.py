import asyncio
from typing import Optional

import click
import rpc


@click.group()
def tool():
    pass


@click.command("cancel", short_help="Cancel pending offers")
@click.option(
    "-wp",
    "--wallet-rpc-port",
    help="Set the port where the Wallet is hosting the RPC interface. See the rpc_port under wallet in config.yaml",
    type=int,
    default=None,
)
@click.option("-f", "--fingerprint", help="Set the fingerprint to specify which wallet to use", type=int)
@click.option("-i","--asset_id", type=str, help='The HEX ID of a CAT or NFT. All offers related to this CAT or NFT will be cancelled', default='xch')
@click.option("-a","--cancel_all", type=bool, help='True for cancelling all offers', default=False)
@click.option("-m","--fee", type=int, help='Transaction fee (in MOJO) for each cancellation. Default is 0.', default=0)
@click.option("-d","--dry_run", type=bool, help='A dry run of the cancellation, no offer will be cancelled.', default=False)
def cancel(wallet_rpc_port: Optional[int], fingerprint: int, asset_id: str, cancel_all: bool, fee: int, dry_run: bool):
    if not fingerprint:
        print("--fingerprint is required.")
        return
    if not cancel_all and not asset_id:
        print("You need to provide --asset_id or use --cancel_all option")
        return
    if asset_id.startswith("0x") or asset_id.startswith("0X"):
        asset_id = asset_id[2:]
    asyncio.run(rpc.cancel_offers(asset_id, cancel_all, wallet_rpc_port, fingerprint, fee, dry_run))


tool.add_command(cancel)


if __name__ == '__main__':
    tool()
