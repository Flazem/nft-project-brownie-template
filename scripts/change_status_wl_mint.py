from brownie import NFT, network
from web3 import Web3
from scripts.deploy import deploy_contracts, get_account


def turn_whitelist_mint():
    account = get_account()
    nft_contract = NFT[-1]
    tx = nft_contract.turnWhitelistMint({"from": account})
    tx.wait(1)
    print("Mint for whitelisters is open!")


def main():
    if network.show_active() == "development":
        deploy_contracts(
            name="Test",
            symbol="tst",
            max_total_supply=3333,
            max_per_wallet=2,
            publish=False,
        )
    turn_whitelist_mint()
