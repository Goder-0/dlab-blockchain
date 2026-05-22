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

    append_mined_block(
        chain,
        txs=[{"from": "alice", "to": "bob", "amount": 5}],
        difficulty=difficulty,
    )
    append_mined_block(
        chain,
        txs=[{"from": "bob", "to": "charlie", "amount": 2}],
        difficulty=difficulty,
    )

    print_chain(chain)
    ok, reason = is_chain_valid(chain, difficulty=difficulty)
    print("\n검증 결과(변조 전):", ok, reason)

    chain[1]["txs"][0]["amount"] = 9999
    ok, reason = is_chain_valid(chain, difficulty=difficulty)
    print("검증 결과(변조 후):", ok, reason)


if __name__ == "__main__":
    main()
