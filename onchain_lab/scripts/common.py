import os

from dotenv import load_dotenv
from web3 import Web3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT, ".env")


def load_env():
    load_dotenv(ENV_PATH)


def require_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"missing env: {name}")
    return value


def make_web3():
    load_env()
    rpc_url = require_env("RPC_URL")
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise RuntimeError("rpc connection failed")
    return w3


def get_account(w3):
    private_key = require_env("PRIVATE_KEY")
    return w3.eth.account.from_key(private_key)


def get_address(name):
    return Web3.to_checksum_address(require_env(name))


def build_tx_base(w3, account, gas):
    latest = w3.eth.get_block("latest")
    base_fee = latest.get("baseFeePerGas", w3.to_wei("1", "gwei"))
    priority_fee = w3.to_wei("1", "gwei")

    return {
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "chainId": w3.eth.chain_id,
        "gas": gas,
        "maxFeePerGas": base_fee * 2 + priority_fee,
        "maxPriorityFeePerGas": priority_fee,
    }


def send_contract_call(contract_fn, w3, account, gas):
    tx = contract_fn.build_transaction(build_tx_base(w3, account, gas))
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    return tx_hash.hex(), receipt
