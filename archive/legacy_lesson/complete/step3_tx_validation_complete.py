import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LESSON_DIR = os.path.dirname(CURRENT_DIR)
if LESSON_DIR not in sys.path:
    sys.path.append(LESSON_DIR)

from blockchain_core import (  # noqa: E402
    append_mined_block,
    build_balances,
    create_genesis_block,
    filter_valid_transactions,
    is_chain_valid,
    send_tx_to_live_board,
)

SEND_TO_LIVE_BOARD = False
LIVE_BOARD_URL = "http://127.0.0.1:5000"
STUDENT_NAME = "teacher-demo"


def main():
    difficulty = 3
    chain = [create_genesis_block(difficulty=difficulty)]

    tx_pool = [
        {"from": "alice", "to": "bob", "amount": 10},
        {"from": "alice", "to": "dave", "amount": 999},
        {"from": "bob", "to": "alice", "amount": 3},
        {"from": "eve", "to": "alice", "amount": 1},
        {"from": "network", "to": "class_reward", "amount": 5},
    ]

    print("초기 잔액:", build_balances(chain))

    balances = build_balances(chain)
    accepted, rejected, _ = filter_valid_transactions(tx_pool, balances)

    print("\n[채택 거래]")
    for tx in accepted:
        print(tx)

    print("\n[거절 거래]")
    for item in rejected:
        print(item)

    if accepted:
        append_mined_block(chain, txs=accepted, difficulty=difficulty)

    print("\n최종 잔액:", build_balances(chain))
    ok, reason = is_chain_valid(chain, difficulty=difficulty)
    print("체인 검증:", ok, reason)

    if SEND_TO_LIVE_BOARD and accepted:
        print(f"\n[라이브보드 전송] target={LIVE_BOARD_URL}")
        for tx in accepted:
            ok, result = send_tx_to_live_board(
                server_url=LIVE_BOARD_URL,
                sender=tx["from"],
                receiver=tx["to"],
                amount=tx["amount"],
                student=STUDENT_NAME,
            )
            if ok:
                print("전송 성공:", result.get("tx"), "pending=", result.get("pending_count"))
            else:
                print("전송 실패:", result)


if __name__ == "__main__":
    main()
