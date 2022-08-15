from brownie import NFT, network
from scripts.deploy import deploy_contracts, get_account
from variables_for_project import tresuare_amount


def tresuare_mint(amount):
    account = get_account()
    nft_contract = NFT[-1]
    tx = nft_contract.tresuareMint(amount, {"from": account})
    tx.wait(1)
    print(f"{amount} tokens were minted for the team!")


def main():
    if network.show_active() == "development":
        deploy_contracts(
            name="Test",
            symbol="tst",
            max_total_supply=3333,
            max_per_wallet=2,
            publish=False,
        )
    tresuare_mint(tresuare_amount)
