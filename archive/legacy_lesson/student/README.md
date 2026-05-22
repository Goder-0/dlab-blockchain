# Student Lesson (배포용)

타이핑 부담을 줄이되, 학생이 직접 해보는 감각을 위해
`TODO`를 채우는 형태로 구성했습니다.

## 파일

- `step1_hash_playground_student.py`: 해시 실습 TODO 버전
- `step2_chain_link_student.py`: 체인 연결/변조 실습 TODO 버전
- `optional_pow_mining_student.py`: PoW 채굴 시간 실습 TODO 버전
- `step3_tx_validation_student.py`: 거래 검증 + 라이브보드 전송 확장판

## 사용 방법

1. 선생님이 `live_board/server.py`를 실행합니다.
2. 학생은 각 파일의 `TODO`를 채웁니다.
3. 아래 명령으로 실행합니다.

```bash
python3 lesson/student/step1_hash_playground_student.py
python3 lesson/student/step2_chain_link_student.py
```

`step3` 흐름 기반으로 실행:

```bash
python3 lesson/student/step3_tx_validation_student.py
```

현재 수업 기준 기본 흐름은 `step1`, `step2`, `step3`입니다.
`optional_pow_mining`은 PoW/채굴 개념을 별도로 다룰 때 사용하는 보조 실습입니다.

## TODO 실습 포인트

- `step1`: 한 글자 변경, 해시 함수 호출 결과 비교
- `step2`: 거래 블록 추가, 변조 값 입력 후 검증 실패 확인
- `optional_pow_mining`: 난이도 리스트 변경, 시간/nonce 비교 (선택)
- `step3`: 거래 입력값 변경 + (선택) 라이브보드 전송
