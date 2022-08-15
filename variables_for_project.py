"""
In this file, you can specify all the variables that are necessary 
to deploy the contract on the network
"""
# This variable is responsible for the name of the project.
# For example "Bored Ape Yacht Club"
name = "Bored Template"

# This variable is responsible for the symbol of the project.
# For example "BAYC"
symbol = "BT"

# This variable is responsible for the maximum number of
# tokens that can be minted.
max_total_supply = 3333

# This variable is responsible for the maximum number of
# tokens that a user can mint.
max_per_wallet = 2

# This variable determines if you want your contract
# to be verified for etherscan.
publish = True

# This variable must be assigned the base URI
baseURI = "google.com/"

# These variables are responsible for the prices
# you want to set for different phases of the mint
allowlist_price = 0.003  # in ETH
public_price = 0.009  # in ETH

# Number of tokens you want to mint for a team
tresuare_amount = 100


# Number of tokens you want to mint for a team
tresuare_amount = 100

# Whitelist addresses. Either the names of the
# file in which they are located (the file must be
# in the root of the project), or an array with addresses.
whitelist = "whitelist_address.txt"
# or ['0x5B38Da6a701c568545dCfcB03FcB875f56beddC4','0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'...]


# Allowlist addresses.
allowlist = "allowlist_address.txt"
# or ['0x5B38Da6a701c568545dCfcB03FcB875f56beddC4','0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'...]
