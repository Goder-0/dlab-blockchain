import os
import sys
from datetime import date

from flask import Flask, abort, jsonify, request, send_from_directory

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LESSON_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "lesson")
ONCHAIN_SCRIPTS_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "onchain_lab", "scripts")
if LESSON_DIR not in sys.path:
    sys.path.append(LESSON_DIR)
if ONCHAIN_SCRIPTS_DIR not in sys.path:
    sys.path.append(ONCHAIN_SCRIPTS_DIR)

from blockchain_core import (  # noqa: E402
    append_mined_block,
    is_chain_valid,
    mine_block,
)
from common import get_account, get_address, load_env, make_web3, send_contract_call  # noqa: E402

app = Flask(__name__, static_folder="static")

TRANSACTION_LEDGER_ABI = [
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
]

CERTIFICATE_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "string", "name": "learnerAlias", "type": "string"},
            {"internalType": "string", "name": "courseTitle", "type": "string"},
            {"internalType": "string", "name": "issuedAtLabel", "type": "string"},
            {"internalType": "string", "name": "tokenUri_", "type": "string"},
        ],
        "name": "issueCertificate",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "recipient", "type": "address"}],
        "name": "tokenOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

CLASSROOM_RULES = {
    "tx_fee": 1,
    "max_balance": 60,
    "default_balance": 20,
    "accounts": {
        "atlas-01": 20,
        "blaze-02": 20,
        "comet-03": 20,
        "drift-04": 20,
        "ember-05": 20,
        "frost-06": 20,
        "glint-07": 20,
        "harbor-08": 20,
        "ion-09": 20,
        "jade-10": 20,
    },
}

STATE = {
    "difficulty": 3,
    "chain": [],
    "pending_txs": [],
}


def reset_chain():
    genesis_txs = [
        {"from": "network", "to": name, "amount": amount, "fee": 0}
        for name, amount in CLASSROOM_RULES["accounts"].items()
    ]
    STATE["chain"] = [
        mine_block(index=0, txs=genesis_txs, prev_hash="0" * 64, difficulty=STATE["difficulty"])
    ]
    STATE["pending_txs"] = []


def _is_teacher_request():
    return request.remote_addr in {"127.0.0.1", "::1"}


def _require_teacher_request():
    if not _is_teacher_request():
        abort(403)


def _account_names():
    return set(CLASSROOM_RULES["accounts"])


def _build_classroom_balances(chain):
    balances = {name: 0 for name in CLASSROOM_RULES["accounts"]}

    for block in chain:
        for tx in block["txs"]:
            sender = tx["from"]
            receiver = tx["to"]
            amount = int(tx["amount"])
            fee = int(tx.get("fee", 0))

            if sender != "network":
                balances[sender] = balances.get(sender, 0) - amount - fee
            balances[receiver] = balances.get(receiver, 0) + amount

    return balances


def _filter_classroom_transactions(txs, balances):
    temp_balances = dict(balances)
    accepted = []
    rejected = []
    known_accounts = _account_names()
    fee = CLASSROOM_RULES["tx_fee"]
    max_balance = CLASSROOM_RULES["max_balance"]

    for tx in txs:
        ok, reason = _validate_single_tx(tx)
        if not ok:
            rejected.append({"tx": tx, "reason": reason})
            continue

        sender = tx["from"]
        receiver = tx["to"]
        amount = int(tx["amount"])

        if sender not in known_accounts or receiver not in known_accounts:
            rejected.append({"tx": tx, "reason": "unknown account"})
            continue
        if sender == receiver:
            rejected.append({"tx": tx, "reason": "sender and receiver must differ"})
            continue
        if temp_balances.get(sender, 0) < amount + fee:
            rejected.append({"tx": tx, "reason": "insufficient balance (including fee)"})
            continue
        if temp_balances.get(receiver, 0) + amount > max_balance:
            rejected.append({"tx": tx, "reason": "receiver would exceed max balance"})
            continue

        temp_balances[sender] = temp_balances.get(sender, 0) - amount - fee
        temp_balances[receiver] = temp_balances.get(receiver, 0) + amount
        accepted.append(
            {
                "from": sender,
                "to": receiver,
                "amount": amount,
                "fee": fee,
                "student_name": tx.get("student_name", ""),
                "onchain_alias": tx.get("onchain_alias", ""),
            }
        )

    return accepted, rejected, temp_balances


def _normalize_tx(raw_tx):
    if not isinstance(raw_tx, dict):
        return None, "tx must be an object"

    sender = str(raw_tx.get("from", "")).strip()
    receiver = str(raw_tx.get("to", "")).strip()
    try:
        amount = int(raw_tx.get("amount"))
    except (TypeError, ValueError):
        return None, "amount must be an integer"

    if sender == "" or receiver == "":
        return None, "from/to must not be empty"
    if amount <= 0:
        return None, "amount must be > 0"

    normalized = {"from": sender, "to": receiver, "amount": amount}
    student_name = str(
        raw_tx.get("student_name", raw_tx.get("student", ""))
    ).strip()
    onchain_alias = str(raw_tx.get("onchain_alias", "")).strip()
    if student_name:
        normalized["student_name"] = student_name
    if onchain_alias:
        normalized["onchain_alias"] = onchain_alias
    return normalized, "ok"


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


def _normalize_account(raw):
    if not isinstance(raw, dict):
        return None, "account must be an object"

    label = str(raw.get("label", "")).strip()
    try:
        initial_balance = int(raw.get("initial_balance", CLASSROOM_RULES["default_balance"]))
    except (TypeError, ValueError):
        return None, "initial_balance must be an integer"

    if label == "":
        return None, "label must not be empty"
    if len(label) > 32:
        return None, "label is too long"
    if initial_balance <= 0:
        return None, "initial_balance must be > 0"
    if initial_balance > CLASSROOM_RULES["max_balance"]:
        return None, "initial_balance exceeds max balance"
    if label in CLASSROOM_RULES["accounts"]:
        return None, "duplicate account"

    return {"label": label, "initial_balance": initial_balance}, "ok"


def _normalize_certificate_request(raw):
    if not isinstance(raw, dict):
        return None, "request must be an object"

    recipient = str(raw.get("recipient", "")).strip()
    learner_alias = str(raw.get("learner_alias", "")).strip()
    course_title = str(raw.get("course_title", "")).strip()
    issued_at = str(raw.get("issued_at", "")).strip()
    token_uri = str(raw.get("token_uri", "")).strip()

    if recipient == "":
        return None, "recipient must not be empty"

    if learner_alias == "":
        learner_alias = f"wallet-{recipient[-6:]}"
    if course_title == "":
        course_title = "Blockchain Special Lecture"
    if issued_at == "":
        issued_at = date.today().isoformat()
    if token_uri == "":
        load_env()
        token_uri = os.getenv("CERTIFICATE_TOKEN_URI", "").strip()

    return {
        "recipient": recipient,
        "learner_alias": learner_alias,
        "course_title": course_title,
        "issued_at": issued_at,
        "token_uri": token_uri,
    }, "ok"


def _onchain_enabled():
    root = os.path.dirname(CURRENT_DIR)
    env_path = os.path.join(root, "onchain_lab", ".env")
    return os.path.exists(env_path)


def _record_onchain_block(accepted, rejected_count, note):
    if not accepted:
        return {"enabled": _onchain_enabled(), "recorded": False, "reason": "no accepted tx"}

    try:
        entries = [
            (
                tx["from"],
                tx["to"],
                int(tx["amount"]),
                str(tx.get("onchain_alias", "")),
            )
            for tx in accepted
        ]
        w3 = make_web3()
        account = get_account(w3)
        contract = w3.eth.contract(
            address=get_address("TRANSACTION_LEDGER_ADDRESS"),
            abi=TRANSACTION_LEDGER_ABI,
        )
        tx_hash, receipt = send_contract_call(
            contract.functions.recordClassBlock(entries, rejected_count, note),
            w3,
            account,
            gas=900000,
        )
        block_count = contract.functions.blockCount().call()
        return {
            "enabled": True,
            "recorded": True,
            "tx_hash": tx_hash,
            "receipt_status": int(receipt.status),
            "block_count": int(block_count),
            "explorer_url": f"https://sepolia.etherscan.io/tx/{tx_hash}",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "enabled": _onchain_enabled(),
            "recorded": False,
            "error": str(exc),
        }


def _mint_onchain_certificate(item):
    try:
        w3 = make_web3()
        account = get_account(w3)
        contract = w3.eth.contract(
            address=get_address("CERTIFICATE_ADDRESS"),
            abi=CERTIFICATE_ABI,
        )
        recipient = w3.to_checksum_address(item["recipient"])
        tx_hash, receipt = send_contract_call(
            contract.functions.issueCertificate(
                recipient,
                item["learner_alias"],
                item["course_title"],
                item["issued_at"],
                item["token_uri"],
            ),
            w3,
            account,
            gas=700000,
        )
        token_id = contract.functions.tokenOf(recipient).call()
        return {
            "ok": True,
            "tx_hash": tx_hash,
            "receipt_status": int(receipt.status),
            "token_id": int(token_id),
            "recipient": recipient,
            "explorer_url": f"https://sepolia.etherscan.io/tx/{tx_hash}",
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


@app.route("/")
def index():
    _require_teacher_request()
    return send_from_directory(app.static_folder, "index.html")


@app.route("/certificates")
def certificates():
    _require_teacher_request()
    return send_from_directory(app.static_folder, "certificate.html")


@app.get("/api/chain")
def get_chain():
    ok, reason = is_chain_valid(STATE["chain"], difficulty=STATE["difficulty"])
    return jsonify(
        {
            "difficulty": STATE["difficulty"],
            "valid": ok,
            "reason": reason,
            "length": len(STATE["chain"]),
            "pending_count": len(STATE["pending_txs"]),
            "chain": STATE["chain"],
        }
    )


@app.get("/api/balances")
def get_balances():
    return jsonify({"balances": _build_classroom_balances(STATE["chain"])})


@app.get("/api/classroom_config")
def get_classroom_config():
    return jsonify(
        {
            "difficulty": STATE["difficulty"],
            "tx_fee": CLASSROOM_RULES["tx_fee"],
            "max_balance": CLASSROOM_RULES["max_balance"],
            "default_balance": CLASSROOM_RULES["default_balance"],
            "accounts": list(CLASSROOM_RULES["accounts"]),
            "initial_balances": CLASSROOM_RULES["accounts"],
        }
    )


@app.get("/api/pending_txs")
def get_pending_txs():
    return jsonify({"count": len(STATE["pending_txs"]), "txs": STATE["pending_txs"]})


@app.post("/api/submit_tx")
def post_submit_tx():
    body = request.get_json(silent=True) or {}
    tx = body.get("tx", body)
    normalized, reason = _normalize_tx(tx)
    if not normalized:
        return jsonify({"ok": False, "error": reason}), 400

    STATE["pending_txs"].append(normalized)
    return jsonify(
        {
            "ok": True,
            "message": "tx queued",
            "pending_count": len(STATE["pending_txs"]),
            "tx": normalized,
        }
    )


@app.post("/api/accounts")
def post_account():
    _require_teacher_request()
    body = request.get_json(silent=True) or {}
    item, reason = _normalize_account(body)
    if not item:
        return jsonify({"ok": False, "error": reason}), 400

    CLASSROOM_RULES["accounts"][item["label"]] = item["initial_balance"]
    grant_tx = {
        "from": "network",
        "to": item["label"],
        "amount": item["initial_balance"],
        "fee": 0,
        "student_name": "teacher-added",
        "onchain_alias": "teacher-added",
    }
    if STATE["chain"]:
        append_mined_block(STATE["chain"], txs=[grant_tx], difficulty=STATE["difficulty"])

    return jsonify(
        {
            "ok": True,
            "account": item,
            "balances": _build_classroom_balances(STATE["chain"]),
            "account_count": len(CLASSROOM_RULES["accounts"]),
        }
    )


@app.post("/api/mint_certificate")
def post_mint_certificate():
    _require_teacher_request()
    body = request.get_json(silent=True) or {}
    item, reason = _normalize_certificate_request(body)
    if not item:
        return jsonify({"ok": False, "error": reason}), 400

    result = _mint_onchain_certificate(item)
    if not result["ok"]:
        return jsonify(result), 400
    return jsonify(result)


@app.post("/api/reset")
def post_reset():
    _require_teacher_request()
    reset_chain()
    return jsonify(
        {
            "ok": True,
            "message": "chain reset",
            "length": len(STATE["chain"]),
            "pending_count": len(STATE["pending_txs"]),
        }
    )


@app.post("/api/mine")
def post_mine():
    _require_teacher_request()
    body = request.get_json(silent=True) or {}
    txs = body.get("txs", [])

    if not isinstance(txs, list):
        return jsonify({"ok": False, "error": "txs must be a list"}), 400

    balances = _build_classroom_balances(STATE["chain"])
    accepted, rejected, _ = _filter_classroom_transactions(txs, balances)

    if not accepted:
        return (
            jsonify(
                {
                    "ok": False,
                    "error": "no valid transactions",
                    "accepted": [],
                    "rejected": rejected,
                }
            ),
            400,
        )

    block = append_mined_block(STATE["chain"], txs=accepted, difficulty=STATE["difficulty"])
    onchain = _record_onchain_block(
        accepted,
        len(rejected),
        f"live-board block #{block['index']}",
    )
    return jsonify(
        {
            "ok": True,
            "block": block,
            "accepted": accepted,
            "rejected": rejected,
            "balances": _build_classroom_balances(STATE["chain"]),
            "onchain": onchain,
        }
    )


@app.post("/api/mine_pending")
def post_mine_pending():
    _require_teacher_request()
    txs = list(STATE["pending_txs"])
    if not txs:
        return jsonify({"ok": False, "error": "pending queue is empty"}), 400

    balances = _build_classroom_balances(STATE["chain"])
    accepted, rejected, _ = _filter_classroom_transactions(txs, balances)

    if not accepted:
        STATE["pending_txs"] = []
        return (
            jsonify(
                {
                    "ok": False,
                    "error": "no valid transactions in pending queue",
                    "accepted": [],
                    "rejected": rejected,
                    "pending_count": 0,
                }
            ),
            400,
        )

    block = append_mined_block(STATE["chain"], txs=accepted, difficulty=STATE["difficulty"])
    onchain = _record_onchain_block(
        accepted,
        len(rejected),
        f"live-board block #{block['index']}",
    )
    STATE["pending_txs"] = []
    return jsonify(
        {
            "ok": True,
            "block": block,
            "accepted": accepted,
            "rejected": rejected,
            "pending_count": 0,
            "balances": _build_classroom_balances(STATE["chain"]),
            "onchain": onchain,
        }
    )


@app.post("/api/difficulty")
def post_difficulty():
    _require_teacher_request()
    body = request.get_json(silent=True) or {}
    value = body.get("difficulty")
    try:
        new_difficulty = int(value)
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "difficulty must be integer"}), 400

    if new_difficulty < 1 or new_difficulty > 6:
        return jsonify({"ok": False, "error": "difficulty range: 1..6"}), 400

    STATE["difficulty"] = new_difficulty
    reset_chain()
    return jsonify(
        {
            "ok": True,
            "message": "difficulty changed and chain reset",
            "difficulty": STATE["difficulty"],
            "pending_count": len(STATE["pending_txs"]),
        }
    )


def main():
    reset_chain()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
