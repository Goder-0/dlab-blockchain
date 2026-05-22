import hashlib
import json
import time
import urllib.error
import urllib.request


def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def calc_hash(index, timestamp, txs, prev_hash, nonce):
    payload = {
        "index": index,
        "timestamp": timestamp,
        "txs": txs,
        "prev_hash": prev_hash,
        "nonce": nonce,
    }
    raw = canonical_json(payload).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def mine_block(index, txs, prev_hash, difficulty=3):
    nonce = 0
    timestamp = time.time()
    prefix = "0" * difficulty

    while True:
        block_hash = calc_hash(index, timestamp, txs, prev_hash, nonce)
        if block_hash.startswith(prefix):
            return {
                "index": index,
                "timestamp": timestamp,
                "txs": txs,
                "prev_hash": prev_hash,
                "nonce": nonce,
                "hash": block_hash,
            }
        nonce += 1


def create_genesis_block(difficulty=3):
    txs = [
        {"from": "network", "to": "teacher", "amount": 100},
        {"from": "network", "to": "alice", "amount": 50},
        {"from": "network", "to": "bob", "amount": 50},
    ]
    return mine_block(index=0, txs=txs, prev_hash="0" * 64, difficulty=difficulty)


def append_mined_block(chain, txs, difficulty=3):
    prev_hash = chain[-1]["hash"]
    next_index = len(chain)
    block = mine_block(next_index, txs, prev_hash, difficulty=difficulty)
    chain.append(block)
    return block


def is_chain_valid(chain, difficulty=3):
    prefix = "0" * difficulty

    for i, block in enumerate(chain):
        recomputed = calc_hash(
            block["index"],
            block["timestamp"],
            block["txs"],
            block["prev_hash"],
            block["nonce"],
        )

        if recomputed != block["hash"]:
            return False, f"block {i}: hash mismatch"

        if not block["hash"].startswith(prefix):
            return False, f"block {i}: invalid PoW prefix"

        if i > 0 and block["prev_hash"] != chain[i - 1]["hash"]:
            return False, f"block {i}: prev_hash link broken"

    return True, "ok"


def build_balances(chain):
    balances = {}
    for block in chain:
        for tx in block["txs"]:
            sender = tx["from"]
            receiver = tx["to"]
            amount = int(tx["amount"])

            if sender != "network":
                balances[sender] = balances.get(sender, 0) - amount
            balances[receiver] = balances.get(receiver, 0) + amount

    return balances


def _validate_single_tx(tx):
    required = {"from", "to", "amount"}
    if not required.issubset(tx):
        return False, "missing keys"

    if tx["from"] == "" or tx["to"] == "":
        return False, "empty account name"

    try:
        amount = int(tx["amount"])
    except (TypeError, ValueError):
        return False, "amount is not an integer"

    if amount <= 0:
        return False, "amount must be > 0"

    return True, "ok"


def filter_valid_transactions(txs, balances):
    temp_balances = dict(balances)
    accepted = []
    rejected = []

    for tx in txs:
        ok, reason = _validate_single_tx(tx)
        if not ok:
            rejected.append({"tx": tx, "reason": reason})
            continue

        sender = tx["from"]
        receiver = tx["to"]
        amount = int(tx["amount"])

        if sender != "network" and temp_balances.get(sender, 0) < amount:
            rejected.append({"tx": tx, "reason": "insufficient balance"})
            continue

        if sender != "network":
            temp_balances[sender] = temp_balances.get(sender, 0) - amount
        temp_balances[receiver] = temp_balances.get(receiver, 0) + amount
        accepted.append({"from": sender, "to": receiver, "amount": amount})

    return accepted, rejected, temp_balances


def send_tx_to_live_board(server_url, sender, receiver, amount, student=""):
    tx = {"from": str(sender).strip(), "to": str(receiver).strip(), "amount": int(amount)}
    if student:
        tx["student"] = str(student).strip()

    if tx["from"] == "" or tx["to"] == "":
        return False, {"error": "from/to must not be empty"}
    if tx["amount"] <= 0:
        return False, {"error": "amount must be > 0"}

    payload = json.dumps(tx).encode("utf-8")
    url = f"{server_url.rstrip('/')}/api/submit_tx"
    req = urllib.request.Request(
        url=url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            body = res.read().decode("utf-8")
            return True, json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return False, {"error": f"HTTPError {e.code}", "body": body}
    except urllib.error.URLError as e:
        return False, {"error": f"URLError: {e.reason}"}
