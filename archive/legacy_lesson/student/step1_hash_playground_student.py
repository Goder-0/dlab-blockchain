import hashlib
import json


def sha256_of(data):
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def main():
    # TODO 1) 두 문장을 비슷하게 적고, 한 글자만 다르게 바꿔보세요.
    text1 = "blockchain class"
    text2 = "blockchain Class"  # 예: "blockchain Class"

    if text2 == "":
        print("TODO: text2 값을 채워주세요. (한 글자만 다르게)")
        return

    msg1 = {"text": text1}
    msg2 = {"text": text2}

    print("[1] 같은 데이터는 같은 해시")
    # TODO 2) 같은 msg1을 두 번 해시해서 출력해보세요.
    print(sha256_of(msg1))
    print(sha256_of(msg1))
    print()

    print("[2] 작은 변경도 해시가 크게 달라짐")
    # TODO 3) msg1, msg2의 해시를 각각 출력해보세요.
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
