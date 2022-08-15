from brownie import (
    NFT,
    exceptions,
)
from scripts.deploy import main, get_account, deploy_contracts
from scripts.merkle_proof.merkle_scripts import merkle_root, get_proof_for_address
from web3 import Web3
import pytest


def test_whitelist_mint():
    # deploying contract
    deploy_contracts(
        name="Test",
        symbol="tst",
        max_total_supply=3333,
        max_per_wallet=200,
        publish=False,
    )
    # get accounts
    owner = get_account()
    accounts = [get_account(i).address for i in range(1, 9)]
    # get contract
    nft_contract = NFT[-1]
    # set merkle root for whitelisters
    merkle_root_wl = merkle_root(accounts)
    tx_set_wl_root = nft_contract.setMerkleRootWhitelist(
        merkle_root_wl, {"from": owner}
    )
    tx_set_wl_root.wait(1)
    # check, that user from wl can't mint
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintWhitelist(
            1, get_proof_for_address(accounts[0], accounts), {"from": accounts[0]}
        )
    # open mint for whitelist
    tx_open_wl_mint = nft_contract.turnWhitelistMint({"from": owner})
    tx_open_wl_mint.wait(1)
    # check that limit is exceeded
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintWhitelist(
            201, get_proof_for_address(accounts[0], accounts), {"from": accounts[0]}
        )
    # check that mint impossible for user not from white list
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintWhitelist(
            200, get_proof_for_address(accounts[0], accounts), {"from": owner}
        )
    # mint process for whitelisters
    for i in range(5):
        tx_mint_wl = nft_contract.mintWhitelist(
            200, get_proof_for_address(accounts[i], accounts), {"from": accounts[i]}
        )
        tx_mint_wl.wait(1)
    # check that mint was successful
    assert nft_contract.ownerOf(1) == accounts[0]
    # check that more mint impossible
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintWhitelist(
            1, get_proof_for_address(accounts[6], accounts), {"from": accounts[6]}
        )


def test_allowlist_mint():
    # deploying contract
    deploy_contracts(
        name="Test",
        symbol="tst",
        max_total_supply=3333,
        max_per_wallet=200,
        publish=False,
    )
    # get accounts
    owner = get_account()
    accounts = [get_account(i).address for i in range(1, 9)]
    # get contract
    nft_contract = NFT[-1]
    # set merkle root for allowlisters
    merkle_root_al = merkle_root(accounts)
    tx_set_al_root = nft_contract.setMerkleRootAllowlist(
        merkle_root_al, {"from": owner}
    )
    tx_set_al_root.wait(1)
    # set price for allowlist
    tx_set_al_price = nft_contract.setAllowlistPrice(
        Web3.toWei(0.009, "ether"), {"from": owner}
    )
    tx_set_al_price.wait(1)
    # check, that user from al can't mint
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintAllowlist(
            1,
            get_proof_for_address(accounts[0], accounts),
            {"from": accounts[0], "amount": Web3.toWei(0.009, "ether")},
        )
    # open mint for allowlist
    tx_open_al_mint = nft_contract.turnAllowlistMint({"from": owner})
    tx_open_al_mint.wait(1)
    # check that limit is exceeded
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintAllowlist(
            201,
            get_proof_for_address(accounts[0], accounts),
            {"from": accounts[0], "amount": Web3.toWei(2, "ether")},
        )
    # check that mint impossible for user not from allow list
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintAllowlist(
            1,
            get_proof_for_address(accounts[0], accounts),
            {"from": owner, "amount": Web3.toWei(0.009, "ether")},
        )
    # check that not enough money
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintAllowlist(
            1,
            get_proof_for_address(accounts[0], accounts),
            {"from": accounts[0], "amount": Web3.toWei(0.008, "ether")},
        )
    # mint process for allowlisters
    for i in range(5):
        tx_mint_al = nft_contract.mintAllowlist(
            200,
            get_proof_for_address(accounts[i], accounts),
            {"from": accounts[i], "amount": Web3.toWei(1.8, "ether")},
        )
        tx_mint_al.wait(1)
    # check that mint was successful
    assert nft_contract.ownerOf(1) == accounts[0]
    # check that more mint impossible
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintAllowlist(
            1,
            get_proof_for_address(accounts[6], accounts),
            {"from": accounts[6], "amount": Web3.toWei(0.009, "ether")},
        )
    # check that only owner can withdraw
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.withdraw(
            {"from": accounts[7]},
        )
    # check that withdraw is correct
    contract_balance = Web3.fromWei(nft_contract.balance(), "ether")
    old_owner_balance = Web3.fromWei(owner.balance(), "ether")
    tx_withdraw = nft_contract.withdraw({"from": owner})
    tx_withdraw.wait(1)
    assert Web3.fromWei(owner.balance(), "ether") == (
        contract_balance + old_owner_balance
    )


def test_public_mint():
    # deploying contract
    deploy_contracts(
        name="Test",
        symbol="tst",
        max_total_supply=3333,
        max_per_wallet=350,
        publish=False,
    )
    # get accounts
    owner = get_account()
    accounts = [get_account(i).address for i in range(1, 10)]
    # get contract
    nft_contract = NFT[-1]
    # set price for public mint
    tx_set_public_price = nft_contract.setPublicPrice(
        Web3.toWei(0.009, "ether"), {"from": owner}
    )
    tx_set_public_price.wait(1)
    # check, that user can't mint
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintPublic(
            1,
            {"from": accounts[0], "amount": Web3.toWei(0.009, "ether")},
        )
    # open public mint
    tx_open_public_mint = nft_contract.turnPublicMint({"from": owner})
    tx_open_public_mint.wait(1)
    # check that limit is exceeded
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintPublic(
            351,
            {"from": accounts[0], "amount": Web3.toWei(5, "ether")},
        )
    # check that not enough money
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintPublic(
            1,
            {"from": accounts[0], "amount": Web3.toWei(0.008, "ether")},
        )
    # mint process
    for i in range(9):
        tx_mint_public = nft_contract.mintPublic(
            350,
            {"from": accounts[i], "amount": Web3.toWei(5, "ether")},
        )
        tx_mint_public.wait(1)
    tx_mint_public = nft_contract.mintPublic(
        183,
        {"from": owner, "amount": Web3.toWei(5, "ether")},
    )
    tx_mint_public.wait(1)
    # check that mint was successful
    assert nft_contract.ownerOf(1) == accounts[0]
    # check that more mint impossible
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.mintPublic(
            1,
            {"from": owner, "amount": Web3.toWei(0.009, "ether")},
        )
    # check that only owner can withdraw
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.withdraw(
            {"from": accounts[7]},
        )
    # check that withdraw is correct
    contract_balance = Web3.fromWei(nft_contract.balance(), "ether")
    old_owner_balance = Web3.fromWei(owner.balance(), "ether")
    tx_withdraw = nft_contract.withdraw({"from": owner})
    tx_withdraw.wait(1)
    assert Web3.fromWei(owner.balance(), "ether") == (
        contract_balance + old_owner_balance
    )
    # check that correct totalSupply
    assert nft_contract.totalSupply() == 3333
    # set baseURI
    tx_set_uri = nft_contract.setBaseURI("google.com/", {"from": owner})
    tx_set_uri.wait(1)
    # check token base uri is correct
    assert nft_contract.tokenURI(100) == "google.com/100"


def test_tresuare_mint():
    # deploying contract
    deploy_contracts(
        name="Test",
        symbol="tst",
        max_total_supply=3333,
        max_per_wallet=350,
        publish=False,
    )
    # get accounts
    owner = get_account()
    accounts = [get_account(i).address for i in range(1, 10)]
    # get contract
    nft_contract = NFT[-1]
    # check, that user can't mint
    with pytest.raises(exceptions.VirtualMachineError):
        nft_contract.tresuareMint(
            1,
            {"from": accounts[0]},
        )
    # owner mint process
    tx_mint_tresuare = nft_contract.tresuareMint(100, {"from": owner})
    tx_mint_tresuare.wait(1)
    # check that mint was successful
    assert nft_contract.ownerOf(1) == owner
