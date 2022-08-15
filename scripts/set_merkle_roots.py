from brownie import NFT, network
from web3 import Web3
from scripts.deploy import deploy_contracts, get_account
from scripts.merkle_proof.merkle_scripts import *
from variables_for_project import whitelist, allowlist


def set_merkle_root_wl():
    account = get_account()
    nft_contract = NFT[-1]
    whitelist_root = merkle_root(whitelist)
    tx = nft_contract.setMerkleRootWhitelist(whitelist_root, {"from": account})
    tx.wait(1)
    print("The merkle root for whitelisters set!")


def set_merkle_root_al():
    account = get_account()
    nft_contract = NFT[-1]
    allowlist_root = merkle_root(allowlist)
    tx = nft_contract.setMerkleRootAllowlist(allowlist_root, {"from": account})
    tx.wait(1)
    print("The merkle root for allowlisters set!")


def main():
    if network.show_active() == "development":
        deploy_contracts(
            name="Test",
            symbol="tst",
            max_total_supply=3333,
            max_per_wallet=2,
            publish=False,
        )
    set_merkle_root_wl()
    set_merkle_root_al()
