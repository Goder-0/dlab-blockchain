# Branch Split Plan

이 저장소는 `main`과 `teacher` 브랜치를 역할별로 나눠 운영하는 것을 전제로 합니다.

중요:
- `teacher` 브랜치도 공개 저장소에서는 technically 공개입니다.
- 따라서 어떤 브랜치에도 `.env`, `PRIVATE_KEY`, 시드 문구는 올리지 않습니다.

## 권장 순서

1. 현재 작업 상태를 `teacher` 브랜치로 먼저 복사
2. `teacher` 브랜치에는 교사용 시연/테스트넷/수료증 발급 코드 유지
3. `main`으로 돌아와 학생용 파일만 남기고 정리

## 1. `main` 브랜치에 남길 것

### 코드
- `lesson/vote_student/`
- 필요하면 `lesson/vote_complete/`

### 학생 안내 문서
- `README.md`  
  학생용 버전으로 교체
- `PPT_SLIDE_PLAN.md`  
  학생 공개용으로 둘지 선택

### 수료증 공개 자산
- `blockchain_certificate.png`
- `certificate_metadata.json`

### 공개 가능 설정 예시
- `.gitignore`
- `onchain_lab/.env.example`

## 2. `main` 브랜치에서 빼거나 숨길 것

- `live_board/`
- `onchain_lab/contracts/ClassTransactionLedger.sol`
- `onchain_lab/contracts/ClassCertificate.sol`
- `onchain_lab/scripts/record_transaction_block.py`
- `onchain_lab/scripts/mint_certificate.py`
- `LESSON_MATERIAL.md`
- `SPECIAL_LECTURE_GUIDE.md`
- `archive/`

학생이 꼭 볼 필요 없는 교사용 자료는 `teacher` 쪽에만 두는 편이 운영상 단순합니다.

## 3. `teacher` 브랜치에 둘 것

### 교사 시연
- `live_board/`

### 테스트넷 / 수료증 발급
- `onchain_lab/contracts/`
- `onchain_lab/scripts/`
- `blockchain_certificate.png`
- `certificate_metadata.json`

### 교사용 문서
- `LESSON_MATERIAL.md`
- `SPECIAL_LECTURE_GUIDE.md`
- `PPT_SLIDE_PLAN.md`
- `README.md`  
  teacher 버전 유지

### 보관 자료
- `archive/`

## 4. 비밀값 원칙

어떤 브랜치에도 아래는 올리지 않습니다.

- `onchain_lab/.env`
- `PRIVATE_KEY`
- MetaMask 시드 문구
- 학생 실명과 지갑 주소의 직접 매핑 파일

## 5. `main`용 README 방향

`main`의 README는 아래 정도만 담는 것이 좋습니다.

- 이 저장소는 학생 실습용
- `lesson/vote_student` 실행 방법
- MetaMask 설치/지갑 만들기 안내
- 제출할 것은 `지갑 주소`뿐이라는 점
- `개인키/시드 문구는 절대 제출하지 말 것`

## 6. `teacher`용 README 방향

`teacher`의 README는 아래를 포함합니다.

- `live_board` 실행
- 테스트넷 연동
- 수료증 발급 페이지 `/certificates`
- `CERTIFICATE_TOKEN_URI` 설정
- 학생 주소 수집 후 발급 절차
