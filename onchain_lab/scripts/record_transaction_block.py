import argparse
import json

from common import get_account, get_address, make_web3, send_contract_call

ABI = [
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "string", "name": "sender", "type": "string"},
                    {"internalType": "string", "name": "receiver", "type": "string"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "string", "name": "studentLabel", "type": "string"},
                ],
                "internalType": "struct ClassTransactionLedger.ClassroomTxInput[]",
                "name": "entries",
                "type": "tuple[]",
            },
            {"internalType": "uint256", "name": "rejectedCount", "type": "uint256"},
            {"internalType": "string", "name": "note", "type": "string"},
        ],
        "name": "recordClassBlock",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "blockCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "label", "type": "string"}],
        "name": "getAccountByLabel",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


def build_parser():
    parser = argparse.ArgumentParser(
        description="Record one accepted classroom transaction block on testnet."
    )
    parser.add_argument(
        "--tx-json",
        required=True,
        help='JSON list like [{"from":"atlas-01","to":"blaze-02","amount":3,"student":"김민수"}]',
    )
    parser.add_argument("--rejected-count", type=int, default=0, help="rejected tx count shown in class")
    parser.add_argument("--note", default="live-board block", help="short block note")
    return parser


def parse_txs(raw_json):
    try:
        txs = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid tx json: {exc}") from exc

    if not isinstance(txs, list) or not txs:
        raise SystemExit("tx-json must be a non-empty JSON list")

    entries = []
    touched = set()

    for tx in txs:
        if not isinstance(tx, dict):
            raise SystemExit("each tx item must be an object")
        sender = str(tx.get("from", "")).strip()
        receiver = str(tx.get("to", "")).strip()
        student = str(tx.get("student", "")).strip()
        try:
            amount = int(tx.get("amount"))
        except (TypeError, ValueError) as exc:
            raise SystemExit("amount must be an integer") from exc

        if sender == "" or receiver == "" or amount <= 0:
            raise SystemExit("each tx needs non-empty from/to and amount > 0")

        entries.append((sender, receiver, amount, student))
        touched.add(sender)
        touched.add(receiver)

    return entries, sorted(touched)


def main():
    args = build_parser().parse_args()
    entries, touched = parse_txs(args.tx_json)

    w3 = make_web3()
    account = get_account(w3)
    contract = w3.eth.contract(address=get_address("TRANSACTION_LEDGER_ADDRESS"), abi=ABI)

    tx_hash, receipt = send_contract_call(
        contract.functions.recordClassBlock(
            entries,
            args.rejected_count,
            args.note,
        ),
        w3,
        account,
        gas=900000,
    )

    block_count = contract.functions.blockCount().call()
    print("tx_hash:", tx_hash)
    print("status:", receipt.status)
    print("block_count:", block_count)

    for label in touched:
        _, balance = contract.functions.getAccountByLabel(label).call()
        print(f"balance[{label}]={balance}")


if __name__ == "__main__":
    main()
