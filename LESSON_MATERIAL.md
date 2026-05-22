# 블록체인 특강 운영안

이 문서는 `학생 실습 -> 교사 시연 -> 수료증 발급` 흐름으로 진행하는 80분 특강 기준 운영안입니다.

## 1. 수업 목표

- 블록체인을 `코인`보다 `기록과 검증` 관점에서 이해한다.
- 아주 쉬운 Python 실습으로 해시, 연결, 검증을 경험한다.
- 교사 시연을 통해 로컬 기록이 실제 테스트넷에도 남을 수 있음을 본다.
- 마지막에 MetaMask 지갑과 수료증 발급으로 블록체인의 활용을 한 번 더 체감한다.

## 2. 사용 코드

### 학생 실습
- `lesson/vote_student/step0_simple_hash_student.py`
- `lesson/vote_student/step1_vote_hash_student.py`
- `lesson/vote_student/step2_vote_chain_student.py`
- `lesson/vote_student/step3_vote_validation_student.py`

### 교사용 완성본
- `lesson/vote_complete/step0_simple_hash_complete.py`
- `lesson/vote_complete/step1_vote_hash_complete.py`
- `lesson/vote_complete/step2_vote_chain_complete.py`
- `lesson/vote_complete/step3_vote_validation_complete.py`

### 교사 시연
- `live_board/server.py`
- `live_board/static/index.html`
- `onchain_lab/contracts/ClassTransactionLedger.sol`

## 3. 80분 구성

### 1. 도입 10분
- 질문: `블록체인 하면 뭐가 떠오르나요?`
- 정리:
  - 코인은 활용 사례 중 하나
  - 오늘은 `믿을 수 있는 기록`에 집중

### 2. 학생 실습 25분
- `step0`: 내가 직접 아주 단순한 해시 함수 만들기
- `step1`: 실제 해시 함수로 같은 기록 / 다른 기록 비교
- `step2`: 이전 해시를 붙여 연결하기
- `step3`: 유효한 표만 채택하기

### 3. 교사 시연 20분
- `live_board`에서 거래 2~3건 등록
- 일부는 성공, 일부는 실패하게 설계
- `채굴 버튼` 클릭
- accepted / rejected 확인
- 테스트넷 기록 완료, `tx hash`, `Etherscan 열기` 확인

### 4. MetaMask + 수료증 15분
- 학생 또는 교사가 MetaMask 테스트넷 지갑 예시 보여주기
- 왜 지갑 주소가 필요한지 설명
- 특강 수료증을 온체인으로 발급하는 흐름 소개
- 실제 발급은 교사 지갑으로 릴레이하거나, 미리 준비한 수료증 컨트랙트에서 진행

### 5. 마무리 질문 10분
- 왜 그냥 메모장/DB가 아니라 검증 가능한 기록이 필요할까?
- 왜 중간 기록을 바꾸면 문제가 될까?
- 왜 잘못된 표나 거래는 거절해야 할까?
- 블록체인은 돈 말고 어디에 쓸 수 있을까?

## 4. 학생 실습에서 강조할 포인트

### step0
- 함수는 입력을 받아 결과를 만든다
- 지금 만든 함수는 너무 단순하다

### step1
- 같은 기록은 같은 해시
- 한 부분만 바꿔도 결과가 달라진다

### step2
- 뒤 기록이 앞 기록에 기대고 있다
- 앞 기록이 바뀌면 뒤도 다시 계산해야 한다

### step3
- 시스템은 표를 다 받지 않는다
- 규칙을 통과한 표만 채택한다

## 5. 교사 시연에서 강조할 포인트

- `live_board`는 학생 실습의 아이디어를 더 큰 시스템처럼 보여주는 화면이다
- accepted 거래만 블록에 들어간다
- rejected 거래는 이유가 있다
- 블록이 만들어진 뒤, 그 결과를 테스트넷에 기록할 수 있다
- 테스트넷 탐색기는 메인 설명 화면이 아니라 `증빙 화면`이다

## 6. 수료증 발급 단계 메모

- 이 단계의 메시지는 `블록체인에 거래만 남기는 것이 아니다`
- 수료증, 배지, 인증서도 온체인 기록 대상으로 설계할 수 있다
- 실명 공개가 부담되면:
  - 별칭
  - 학생 번호
  - 해시 처리된 식별자
  등을 사용

## 7. 특강 기본 메시지

- 블록체인은 돈 기술이 아니라, 여러 사람이 함께 검증할 수 있는 기록 기술이다.
- 시스템은 사람의 말을 그대로 믿지 않고 규칙을 검사한다.
- 좋은 기술은 멋져 보이는 기술이 아니라 문제에 맞는 기술이다.
