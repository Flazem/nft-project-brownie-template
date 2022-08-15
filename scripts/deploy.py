from brownie import NFT, accounts, config, network
from variables_for_project import (
    name,
    symbol,
    max_total_supply,
    max_per_wallet,
    publish,
)


def deploy_contracts(name, symbol, max_total_supply, max_per_wallet, publish=False):
    """
    This function deploys contract to the network.
    By default, contracts are deployed without confirmation in etherscan.
    The publish variable is responsible for this.
    """
    account = get_account()
    nft_contract = NFT.deploy(
        name,
        symbol,
        max_total_supply,
        max_per_wallet,
        {"from": account},
        publish_source=publish,
    )
    print("NFT contract deployed!")


def get_account(index=0):
    """
    This function returns the required account.
    If we work in a development network (for example, ganache), then, if necessary, we need to install
    indexes of the accounts we need (default index 0).
    If we work in test or main networks, then it returns an account using a given private key.
    """
    if network.show_active() == "development":
        return accounts[index]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    if network.show_active() == "development":
        deploy_contracts(
            name="Test",
            symbol="tst",
            max_total_supply=3333,
            max_per_wallet=2,
            publish=False,
        )
    deploy_contracts(name, symbol, max_total_supply, max_per_wallet, publish)
