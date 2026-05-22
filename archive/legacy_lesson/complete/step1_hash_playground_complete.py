import hashlib
import json


def sha256_of(data):
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def main():
    msg1 = {"text": "blockchain class"}
    msg2 = {"text": "blockchain Class"}

    print("[1] 같은 데이터는 같은 해시")
    print(sha256_of(msg1))
    print(sha256_of(msg1))
    print()

    print("[2] 작은 변경도 해시가 크게 달라짐")
    print("msg1:", sha256_of(msg1))
    print("msg2:", sha256_of(msg2))
    print()

    print("[3] 딕셔너리 키 순서가 달라도 같은 의미면 같은 해시")
    data_a = {"txs": [{"from": "alice", "to": "bob", "amount": 3}], "index": 1}
    data_b = {"index": 1, "txs": [{"from": "alice", "to": "bob", "amount": 3}]}
    print("A:", sha256_of(data_a))
    print("B:", sha256_of(data_b))


if __name__ == "__main__":
    main()
