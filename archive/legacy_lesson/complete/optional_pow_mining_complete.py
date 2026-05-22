import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LESSON_DIR = os.path.dirname(CURRENT_DIR)
if LESSON_DIR not in sys.path:
    sys.path.append(LESSON_DIR)

from blockchain_core import mine_block  # noqa: E402


def main():
    txs = [{"from": "alice", "to": "bob", "amount": 1}]
    prev_hash = "0" * 64
    difficulty = 3

    print("채굴 시간 측정")
    start = time.time()
    block = mine_block(1, txs, prev_hash, difficulty=difficulty)
    elapsed = time.time() - start
    print(
        f"difficulty={difficulty} "
        f"nonce={block['nonce']} "
        f"time={elapsed:.3f}s "
        f"hash={block['hash'][:14]}..."
    )

    print("\n난이도를 올리면 평균적으로 채굴 시간이 더 길어집니다.")


if __name__ == "__main__":
    main()
