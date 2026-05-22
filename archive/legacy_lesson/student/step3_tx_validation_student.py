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

# TODO 1) 아래 값만 바꿔서 사용하세요.
SEND_TO_LIVE_BOARD = False
LIVE_BOARD_URL = "http://127.0.0.1:5000"
STUDENT_NAME = ""  # 예: "team1"


def main():
    difficulty = 3
    chain = [create_genesis_block(difficulty=difficulty)]

    # TODO 2) 아래 거래 예시 값을 바꿔보세요.
    # 조건:
    # - 유효 거래 1개 이상
    # - 잔액 부족 거래 1개 이상
    tx_pool = [
        {"from": "alice", "to": "bob", "amount": 5},
        {"from": "alice", "to": "dave", "amount": 999},
        {"from": "bob", "to": "alice", "amount": 2},
    ]

    balances = build_balances(chain)
    accepted, rejected, _ = filter_valid_transactions(tx_pool, balances)

    print("[채택 거래]")
    for tx in accepted:
        print(tx)

    print("\n[거절 거래]")
    for item in rejected:
        print(item)

    if accepted:
        append_mined_block(chain, txs=accepted, difficulty=difficulty)

    ok, reason = is_chain_valid(chain, difficulty=difficulty)
    print("\n체인 검증:", ok, reason)
    print("최종 잔액:", build_balances(chain))

    if SEND_TO_LIVE_BOARD and STUDENT_NAME == "":
        print("\nTODO: STUDENT_NAME을 채워주세요.")
        return

    # TODO 3) 전송 부분은 이미 완성되어 있습니다.
    # 거래값을 바꿔가며 live_board 대기열에 어떻게 쌓이는지 확인해보세요.
    if SEND_TO_LIVE_BOARD:
        print(f"\n[라이브보드 전송] {LIVE_BOARD_URL}")
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
