import argparse

from common import get_account, get_address, make_web3, send_contract_call

ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "author", "type": "string"},
            {"internalType": "string", "name": "message", "type": "string"},
        ],
        "name": "sign",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "length",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]


def build_parser():
    parser = argparse.ArgumentParser(description="Write one classroom guestbook message on testnet.")
    parser.add_argument("--author", required=True, help="team or student label")
    parser.add_argument("--message", required=True, help="short guestbook message")
    return parser


def main():
    args = build_parser().parse_args()

    w3 = make_web3()
    account = get_account(w3)
    contract = w3.eth.contract(address=get_address("GUESTBOOK_ADDRESS"), abi=ABI)

    tx_hash, receipt = send_contract_call(
        contract.functions.sign(args.author, args.message),
        w3,
        account,
        gas=250000,
    )

    total = contract.functions.length().call()
    print("author:", args.author)
    print("message:", args.message)
    print("tx_hash:", tx_hash)
    print("status:", receipt.status)
    print("entry_count:", total)


if __name__ == "__main__":
    main()
