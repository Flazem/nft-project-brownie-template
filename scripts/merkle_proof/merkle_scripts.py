from scripts.merkle_proof.merkletools_instance import MerkleTools


def make_markle_tree(addresses):
    leafs = []
    tree = MerkleTools(hash_type="keccak")
    if type(addresses) == str:
        with open(addresses, mode="r", encoding="utf-8") as in_file:
            for address in in_file:
                tree.add_leaf(address.strip(), True)
                leafs.append(address.strip())
    elif type(addresses) == list:
        for address in addresses:
            tree.add_leaf(address.strip(), True)
            leafs.append(address.strip())
    tree.make_tree()
    return tree, leafs


def merkle_root(addresses):
    tree, *_ = make_markle_tree(addresses)
    return tree.get_merkle_root()


def get_proof_for_address(address, addresses):
    tree, leafs = make_markle_tree(addresses)
    try:
        index_of_target = leafs.index(address)
        proof = tree.get_proof(index_of_target)
        return [
            value if value[0] == "0" else "0x" + value
            for leaf in proof
            for value in leaf.values()
        ]
    except ValueError:
        return "The address is not in the merkle tree!"
