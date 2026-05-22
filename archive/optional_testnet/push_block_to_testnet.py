import os
import sys
import time

from dotenv import load_dotenv
from web3 import Web3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSON_DIR = os.path.join(ROOT, "lesson")
if LESSON_DIR not in sys.path:
    sys.path.append(LESSON_DIR)

from blockchain_core import calc_hash  # noqa: E402

ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "blockHash", "type": "bytes32"},
            {"internalType": "string", "name": "note", "type": "string"},
        ],
        "name": "addBlock",
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


def require_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"missing env: {name}")
    return value


def make_demo_block_hash():
    index = 1
    timestamp = time.time()
    txs = [{"from": "alice", "to": "bob", "amount": 7}]
    prev_hash = "0" * 64
    nonce = 42
    return calc_hash(index, timestamp, txs, prev_hash, nonce)


def main():
    load_dotenv()
    rpc_url = require_env("RPC_URL")
    private_key = require_env("PRIVATE_KEY")
    contract_address = require_env("CONTRACT_ADDRESS")

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise RuntimeError("rpc connection failed")

    acct = w3.eth.account.from_key(private_key)
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=ABI)

    local_hash_hex = make_demo_block_hash()
    block_hash_bytes = bytes.fromhex(local_hash_hex)
    note = "class-demo"

    nonce = w3.eth.get_transaction_count(acct.address)
    tx = contract.functions.addBlock(block_hash_bytes, note).build_transaction(
        {
            "from": acct.address,
            "nonce": nonce,
            "chainId": w3.eth.chain_id,
            "gas": 250000,
            "maxFeePerGas": w3.to_wei("30", "gwei"),
            "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
        }
    )

    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)

    length = contract.functions.length().call()
    print("local_block_hash:", local_hash_hex)
    print("tx_hash:", tx_hash.hex())
    print("status:", receipt.status)
    print("contract_length:", length)


if __name__ == "__main__":
    main()
