import argparse

from web3 import Web3

from common import get_account, get_address, make_web3, send_contract_call

ABI = [
    {
        "inputs": [
            {"internalType": "uint8", "name": "optionIndex", "type": "uint8"},
            {"internalType": "bytes32", "name": "voterIdHash", "type": "bytes32"},
            {"internalType": "string", "name": "voterLabel", "type": "string"},
        ],
        "name": "castVote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "getOption",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalVotesCast",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]


def build_parser():
    parser = argparse.ArgumentParser(description="Relay one classroom vote to testnet.")
    parser.add_argument("--label", required=True, help="student or team label shown in class")
    parser.add_argument("--voter-id", required=True, help="unique id used only to prevent duplicates")
    parser.add_argument("--option", type=int, required=True, help="option index starting at 0")
    return parser


def main():
    args = build_parser().parse_args()

    w3 = make_web3()
    account = get_account(w3)
    contract = w3.eth.contract(address=get_address("VOTE_ADDRESS"), abi=ABI)

    voter_id_hash = Web3.keccak(text=args.voter_id)
    tx_hash, receipt = send_contract_call(
        contract.functions.castVote(args.option, voter_id_hash, args.label),
        w3,
        account,
        gas=250000,
    )

    option_label, option_votes = contract.functions.getOption(args.option).call()
    total_votes = contract.functions.totalVotesCast().call()

    print("label:", args.label)
    print("voter_id_hash:", voter_id_hash.hex())
    print("option_index:", args.option)
    print("option_label:", option_label)
    print("option_votes:", option_votes)
    print("total_votes:", total_votes)
    print("tx_hash:", tx_hash)
    print("status:", receipt.status)


if __name__ == "__main__":
    main()
