import argparse
import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
LESSON_DIR = os.path.join(ROOT, "lesson")

if LESSON_DIR not in sys.path:
    sys.path.append(LESSON_DIR)

from blockchain_core import calc_hash  # noqa: E402
from common import get_account, get_address, make_web3, send_contract_call  # noqa: E402

ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "localBlockHash", "type": "bytes32"},
            {"internalType": "string", "name": "stepLabel", "type": "string"},
            {"internalType": "string", "name": "teamName", "type": "string"},
            {"internalType": "string", "name": "note", "type": "string"},
        ],
        "name": "anchorBlock",
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
    parser = argparse.ArgumentParser(description="Anchor one local lesson block on a testnet.")
    parser.add_argument("--team", required=True, help="team or student label")
    parser.add_argument("--step", default="step3", help="lesson step label")
    parser.add_argument("--note", default="lesson-demo", help="short note stored on-chain")
    parser.add_argument("--sender", default="alice", help="demo tx sender")
    parser.add_argument("--receiver", default="bob", help="demo tx receiver")
    parser.add_argument("--amount", type=int, default=7, help="demo tx amount")
    return parser


def make_demo_block_hash(sender, receiver, amount):
    index = 1
    timestamp = time.time()
    txs = [{"from": sender, "to": receiver, "amount": amount}]
    prev_hash = "0" * 64
    nonce = 42
    return calc_hash(index, timestamp, txs, prev_hash, nonce)


def main():
    args = build_parser().parse_args()

    w3 = make_web3()
    account = get_account(w3)
    contract = w3.eth.contract(address=get_address("BLOCK_ANCHOR_ADDRESS"), abi=ABI)

    local_hash_hex = make_demo_block_hash(args.sender, args.receiver, args.amount)
    block_hash_bytes = bytes.fromhex(local_hash_hex)

    tx_hash, receipt = send_contract_call(
        contract.functions.anchorBlock(block_hash_bytes, args.step, args.team, args.note),
        w3,
        account,
        gas=300000,
    )

    total = contract.functions.length().call()
    print("local_block_hash:", local_hash_hex)
    print("team:", args.team)
    print("tx_hash:", tx_hash)
    print("status:", receipt.status)
    print("contract_length:", total)


if __name__ == "__main__":
    main()
