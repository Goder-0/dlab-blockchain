import argparse
import json
import urllib.error
import urllib.request


def ask_if_empty(value, prompt):
    if value is not None:
        return value
    return input(prompt).strip()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Send one transaction to teacher's live_board server."
    )
    parser.add_argument("--server", help="e.g. http://192.168.0.20:5000")
    parser.add_argument("--from", dest="sender", help="sender account name")
    parser.add_argument("--to", dest="receiver", help="receiver account name")
    parser.add_argument("--amount", type=int, help="positive integer")
    parser.add_argument("--name", help="local display name (optional)")
    parser.add_argument("--alias", help="testnet alias (optional)")
    parser.add_argument("--student", help="legacy local display name (optional)")
    return parser


def post_json(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as res:
        body = res.read().decode("utf-8")
        return res.status, json.loads(body)


def main():
    parser = build_parser()
    args = parser.parse_args()

    server = ask_if_empty(args.server, "Teacher server URL: ").rstrip("/")
    sender = ask_if_empty(args.sender, "from: ")
    receiver = ask_if_empty(args.receiver, "to: ")

    amount = args.amount
    if amount is None:
        amount = int(ask_if_empty(None, "amount (int): "))

    if sender == "" or receiver == "" or amount <= 0:
        raise SystemExit("invalid input: from/to required, amount > 0")

    payload = {"from": sender, "to": receiver, "amount": amount}
    local_name = args.name or args.student
    if local_name:
        payload["student_name"] = local_name
    if args.alias:
        payload["onchain_alias"] = args.alias

    url = f"{server}/api/submit_tx"
    try:
        status, response = post_json(url, payload)
        print("status:", status)
        print("queued_tx:", response.get("tx"))
        print("pending_count:", response.get("pending_count"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print("HTTPError:", e.code, body)
    except urllib.error.URLError as e:
        print("URLError:", e.reason)


if __name__ == "__main__":
    main()
