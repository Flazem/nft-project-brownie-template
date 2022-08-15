from brownie import NFT, network
from web3 import Web3
from scripts.deploy import deploy_contracts, get_account
from variables_for_project import allowlist_price, public_price


def set_price_for_allowlist(price):
    account = get_account()
    nft_contract = NFT[-1]
    tx = nft_contract.setAllowlistPrice(Web3.toWei(price, "ether"), {"from": account})
    tx.wait(1)
    print("The sell price for allowlisters set!")


def set_price_for_public(price):
    account = get_account()
    nft_contract = NFT[-1]
    tx = nft_contract.setPublicPrice(Web3.toWei(price, "ether"), {"from": account})
    tx.wait(1)
    print("The sell price for public mint set!")


def main():
    if network.show_active() == "development":
        deploy_contracts(
            name="Test",
            symbol="tst",
            max_total_supply=3333,
            max_per_wallet=2,
            publish=False,
        )
    set_price_for_allowlist(allowlist_price)
    set_price_for_public(public_price)
