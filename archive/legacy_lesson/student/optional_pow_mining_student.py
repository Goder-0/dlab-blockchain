import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LESSON_DIR = os.path.dirname(CURRENT_DIR)
if LESSON_DIR not in sys.path:
    sys.path.append(LESSON_DIR)

from blockchain_core import mine_block  # noqa: E402


def main():
    # TODO 1) 거래 데이터(txs)를 원하는 값으로 바꿔보세요.
    txs = [{"from": "alice", "to": "bob", "amount": 1}]
    prev_hash = "0" * 64

    # TODO 2) 난이도 숫자를 바꿔보세요. 예: 2, 3, 4
    difficulty = 4

    print("채굴 시간 측정")
    # TODO 3) 아래 채굴 시간을 직접 측정해보세요.
    start = time.time()
    block = mine_block(1, txs, prev_hash, difficulty=difficulty)
    elapsed = time.time() - start

    print(
        f"difficulty={difficulty} "
        f"nonce={block['nonce']} "
        f"time={elapsed:.3f}s "
        f"hash={block['hash'][:14]}..."
    )

    print("\n질문: 난이도를 1 올리면 채굴 시간이 얼마나 달라질까요?")


if __name__ == "__main__":
    main()
