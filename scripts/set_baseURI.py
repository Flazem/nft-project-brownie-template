from brownie import NFT, network
from scripts.deploy import deploy_contracts, get_account
from variables_for_project import baseURI


def set_baseURI(uri):
    account = get_account()
    nft_contract = NFT[-1]
    tx = nft_contract.setBaseURI(uri, {"from": account})
    tx.wait(1)
    print("Base URI was set!")


def main():
    if network.show_active() == "development":
        deploy_contracts(
            name="Test",
            symbol="tst",
            max_total_supply=3333,
            max_per_wallet=2,
            publish=False,
        )
    set_baseURI(baseURI)
