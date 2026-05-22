# Optional: Testnet On-Chain Practice

이 디렉토리는 초기 테스트넷 프로토타입입니다.

현재는 `../onchain_lab/`을 기준으로 수업을 확장하는 것을 권장합니다.
`onchain_lab/`에는 아래가 정리되어 있습니다.

- `LocalBlockAnchor.sol`
- `ClassVote.sol`
- `ClassGuestbook.sol`
- 공통 Python 스크립트
- 추후 학생용 UI를 둘 위치

로컬에서 만든 블록 해시를 EVM 테스트넷 컨트랙트에 기록하는 확장 실습입니다.

## 학습 목표

- "내가 만든 데이터 해시가 실제 블록체인에 기록된다"를 체감
- 로컬 실습(해시/체인/PoW)과 온체인 저장의 연결 이해

## 준비

1) Python 의존성

```bash
python3 -m pip install web3 python-dotenv
```

2) 환경 변수 파일 생성

```bash
cp .env.example .env
```

`.env` 값을 채우세요:

- `RPC_URL`: 테스트넷 RPC 주소
- `PRIVATE_KEY`: 테스트용 지갑 개인키
- `CONTRACT_ADDRESS`: 배포한 컨트랙트 주소

주의: 테스트넷 전용 키를 사용하세요. 소액의 테스트 토큰(가스비)이 필요합니다.

## 컨트랙트 배포

- `SimpleClassChain.sol`을 Remix 또는 Hardhat으로 테스트넷 배포
- 배포 후 `CONTRACT_ADDRESS`를 `.env`에 입력

## 실행

```bash
python3 push_block_to_testnet.py
```

성공 시 트랜잭션 해시와 저장된 블록 인덱스가 출력됩니다.

## 수업 운영 팁

- 학생별로 `note` 값을 다르게 넣어 이벤트 로그를 비교
- 같은 로컬 블록 해시를 여러 번 넣었을 때 기록이 어떻게 쌓이는지 확인
- "온체인에는 계산 자체보다 결과(증거)를 남긴다"는 메시지 강조
