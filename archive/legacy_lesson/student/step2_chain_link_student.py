import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LESSON_DIR = os.path.dirname(CURRENT_DIR)
if LESSON_DIR not in sys.path:
    sys.path.append(LESSON_DIR)

from blockchain_core import append_mined_block, create_genesis_block, is_chain_valid  # noqa: E402


def print_chain(chain):
    print("\n=== CHAIN ===")
    for b in chain:
        print(
            f"index={b['index']} prev={b['prev_hash'][:10]}... "
            f"hash={b['hash'][:10]}... txs={b['txs']}"
        )


def main():
    difficulty = 3
    chain = [create_genesis_block(difficulty=difficulty)]

    # TODO 1) 아래 두 거래를 추가하고 블록을 채굴해보세요.
    tx1 = {"from": "alice", "to": "bob", "amount": 5}
    tx2 = {"from": "bob", "to": "charlie", "amount": 2}

    append_mined_block(chain, txs=[tx1], difficulty=difficulty)
    append_mined_block(chain, txs=[tx2], difficulty=difficulty)

    print_chain(chain)
    ok, reason = is_chain_valid(chain, difficulty=difficulty)
    print("\n검증 결과(변조 전):", ok, reason)

    # TODO 2) amount 값을 다른 숫자로 바꿔서 변조를 시도해보세요.
    tampered_amount = None  # 예: 9999
    if tampered_amount is None:
        print("TODO: tampered_amount 값을 채워서 변조 실험을 완료하세요.")
        return

    chain[1]["txs"][0]["amount"] = tampered_amount
    ok, reason = is_chain_valid(chain, difficulty=difficulty)
    print("검증 결과(변조 후):", ok, reason)


if __name__ == "__main__":
    main()
