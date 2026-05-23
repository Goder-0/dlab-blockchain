# Python Blockchain Special Lecture Kit

초6~고등 대상 블록체인 특강용 저장소입니다.  
현재 기준 핵심 흐름은 아래 3단계입니다.

1. `lesson/vote_student/`로 아주 쉬운 Python 실습
2. `live_board/`로 교사가 거래 검증, 블록 생성, 테스트넷 기록 시연
3. MetaMask 지갑 생성 후 특강 수료증 발급 단계로 확장

## 현재 사용하는 폴더

- `lesson/vote_student/`: 학생 실습용 아주 쉬운 반장 선거 서사
- `lesson/vote_complete/`: 교사용 정답/완성본
- `live_board/server.py`: 교사용 시연 서버
- `live_board/static/index.html`: 교사용 보드
- `live_board/student_send_tx.py`: 필요할 때만 쓰는 보조 전송 스크립트
- `onchain_lab/contracts/ClassTransactionLedger.sol`: `live_board` 결과를 Sepolia에 기록하는 컨트랙트
- `onchain_lab/contracts/ClassCertificate.sol`: 특강 수료증 발급용 컨트랙트
- `onchain_lab/scripts/record_transaction_block.py`: 테스트넷 기록 스크립트
- `onchain_lab/scripts/mint_certificate.py`: 수료증 민팅 스크립트

## 학생 실습 순서

```bash
python3 lesson/vote_student/step0_simple_hash_student.py
python3 lesson/vote_student/step1_vote_hash_student.py
python3 lesson/vote_student/step2_vote_chain_student.py
python3 lesson/vote_student/step3_vote_validation_student.py
```

정답/완성본:

```bash
python3 lesson/vote_complete/step0_simple_hash_complete.py
python3 lesson/vote_complete/step1_vote_hash_complete.py
python3 lesson/vote_complete/step2_vote_chain_complete.py
python3 lesson/vote_complete/step3_vote_validation_complete.py
```

## 교사 시연 보드 실행

1. 의존성 설치

```bash
python3 -m pip install flask
```

2. 서버 실행

```bash
python3 live_board/server.py
```

3. 브라우저 접속

- 기본: `http://127.0.0.1:5000`
- 포트를 바꿨다면 해당 포트로 접속

`live_board`는 교사용 화면입니다.  
로컬호스트에서만 채굴, 초기화, 난이도 변경, 계정 추가가 가능합니다.

같은 화면에서 학생 지갑 주소를 넣고 수료증 발급도 할 수 있습니다.

## live_board 시연 핵심

- 학생 이름은 한글로 표시 가능
- 테스트넷에는 별칭만 기록 가능
- 채굴 버튼을 누르면:
  - 로컬 블록 생성
  - accepted / rejected 거래 구분
  - Sepolia 테스트넷 기록 시도
  - `tx hash`, 탐색기 링크 표시
- 수료증 발급은 `/certificates` 전용 페이지에서:
  - 학생 지갑 주소만 입력
  - 나머지 값은 기본값 사용
  - 바로 민팅 가능
  - 발급 후 `Blockscout에서 수료증 보기`로 이미지 확인 가능

## 테스트넷 연결

`onchain_lab/.env`에 아래 값이 필요합니다.

- `RPC_URL`
- `PRIVATE_KEY`
- `TRANSACTION_LEDGER_ADDRESS`
- `CERTIFICATE_ADDRESS`

현재 `live_board`는 `ClassTransactionLedger.sol`과 연결되어 있습니다.

중요:
- `PRIVATE_KEY`는 절대 GitHub에 올리지 않습니다.
- `onchain_lab/.env`는 로컬 전용 파일로만 사용합니다.
- 공개 저장소에는 `onchain_lab/.env.example`만 올립니다.
- 지갑 주소는 공개 가능할 수 있지만, 학생 실명과 직접 매핑되는 정보는 신중히 다루는 편이 좋습니다.

수료증 이미지 연결 방식:
- `blockchain_certificate.png`를 GitHub에 올립니다.
- `certificate_metadata.json`의 `image` 값을 해당 GitHub raw URL로 바꿉니다.
- `onchain_lab/.env`의 `CERTIFICATE_TOKEN_URI`에 metadata JSON의 raw URL을 넣습니다.
- 그러면 `/certificates` 페이지에서는 지갑 주소만 입력해도 기본 metadata URL이 같이 들어갑니다.

현재 수료증 컨트랙트:
- `0x3DCa45584025Ede440e0F8F84e10c85B83434173`
- Blockscout: `https://eth-sepolia.blockscout.com/token/0x3DCa45584025Ede440e0F8F84e10c85B83434173`

## 문서

- [LESSON_MATERIAL.md](/Users/kai/Desktop/dlab/blockchain/LESSON_MATERIAL.md:1)
  특강 운영안
- [SPECIAL_LECTURE_GUIDE.md](/Users/kai/Desktop/dlab/blockchain/SPECIAL_LECTURE_GUIDE.md:1)
  교사용 설명 포인트
- [PPT_SLIDE_PLAN.md](/Users/kai/Desktop/dlab/blockchain/PPT_SLIDE_PLAN.md:1)
  AI/NotebookLM용 슬라이드 구성 문서

## 정리된 파일

이번 특강 흐름에서 직접 쓰지 않는 예전 코드와 확장 자료는 `archive/`로 옮겨 두었습니다.

- `archive/legacy_lesson/`: 예전 거래/PoW 학생 실습
- `archive/live_board_student_pages/`: 학생용 보조 HTML
- `archive/onchain_extensions/`: 투표/방명록/앵커 확장 컨트랙트와 스크립트
- `archive/optional_testnet/`: 초기 테스트넷 프로토타입
- `archive/optional_testnet_copy/`: 초기 테스트넷 복사본

## GitHub 브랜치 권장 구조

- `main`
  - 학생에게 제공할 코드
  - 비밀값 없는 문서
- `teacher`
  - `live_board`
  - 교사용 문서
  - 테스트넷 운영용 코드
  - 단, 여기도 `.env`와 private key는 올리지 않음
