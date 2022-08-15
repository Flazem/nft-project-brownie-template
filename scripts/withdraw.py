from brownie import NFT, network
from scripts.deploy import deploy_contracts, get_account


def withdraw():
    account = get_account()
    nft_contract = NFT[-1]
    tx = nft_contract.withdraw({"from": account})
    tx.wait(1)
    print(f"All funds have been withdrawn!")


def main():
    if network.show_active() == "development":
        deploy_contracts(
            name="Test",
            symbol="tst",
            max_total_supply=3333,
            max_per_wallet=2,
            publish=False,
        )
    withdraw()
