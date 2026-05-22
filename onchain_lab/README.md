# On-Chain Lab

이 폴더는 현재 특강에서 `교사 시연용 테스트넷 기록`에만 사용합니다.

## 현재 사용하는 파일

- `contracts/ClassTransactionLedger.sol`
- `contracts/ClassCertificate.sol`
- `contracts/Owned.sol`
- `scripts/common.py`
- `scripts/record_transaction_block.py`
- `scripts/mint_certificate.py`
- `.env`
- `requirements.txt`

## 현재 역할

`live_board`에서 채굴 성공한 거래 묶음을 Sepolia에 기록합니다.

그리고 특강 마지막 단계에서 학생 지갑 주소로 수료증을 발급합니다.

즉 수업 흐름은:

1. 학생은 로컬 Python 실습
2. 교사는 `live_board`에서 블록 생성 시연
3. accepted 거래를 `ClassTransactionLedger`에 기록
4. `tx hash`와 탐색기로 증빙 확인
5. 학생 지갑 주소를 받아 `ClassCertificate`로 수료증 발급

## 준비

```bash
python3 -m pip install -r onchain_lab/requirements.txt
cp onchain_lab/.env.example onchain_lab/.env
```

`.env`에 필요한 값:

- `RPC_URL`
- `PRIVATE_KEY`
- `TRANSACTION_LEDGER_ADDRESS`
- `CERTIFICATE_ADDRESS`
- `CERTIFICATE_TOKEN_URI`

## 기록 스크립트 예시

```bash
python3 onchain_lab/scripts/record_transaction_block.py \
  --tx-json '[{"from":"atlas-01","to":"blaze-02","amount":3,"student":"학생01"}]' \
  --rejected-count 1 \
  --note "live-board block"
```

## 수료증 발급 예시

```bash
python3 onchain_lab/scripts/mint_certificate.py \
  --recipient 0xStudentWalletAddress \
  --alias 학생01 \
  --course-title "Blockchain Special Lecture" \
  --issued-at 2026-05-23
```

이 스크립트는 학생 지갑 주소를 하나씩 받아 수료증을 발급하는 구조입니다.
지갑 주소는 수업 중 MetaMask에서 복사해 교사가 수집하면 됩니다.

## 수료증 이미지 연결

추천 방식은 GitHub에 이미지와 metadata JSON을 같이 올리는 것입니다.

1. `blockchain_certificate.png`를 저장소에 둡니다.
2. `certificate_metadata.json`의 `image`를 GitHub raw URL로 수정합니다.
3. `CERTIFICATE_TOKEN_URI`에 `certificate_metadata.json`의 raw URL을 넣습니다.

예:

```text
https://raw.githubusercontent.com/<owner>/<repo>/main/certificate_metadata.json
```

이 값을 넣어두면 웹 발급 페이지에서는 지갑 주소만 입력해도 동일한 수료증 이미지를 가진 토큰이 발급됩니다.

## 참고

이번 특강 흐름에서 직접 쓰지 않는 예전 확장 컨트랙트와 스크립트는 `archive/onchain_extensions/`로 옮겨 두었습니다.
