import argparse
import json
from datetime import date

from common import get_account, get_address, make_web3, send_contract_call

CERTIFICATE_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "string", "name": "learnerAlias", "type": "string"},
            {"internalType": "string", "name": "courseTitle", "type": "string"},
            {"internalType": "string", "name": "issuedAtLabel", "type": "string"},
            {"internalType": "string", "name": "tokenUri_", "type": "string"},
        ],
        "name": "issueCertificate",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "recipient", "type": "address"}],
        "name": "tokenOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "getCertificate",
        "outputs": [
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "string", "name": "", "type": "string"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


def build_parser():
    parser = argparse.ArgumentParser(
        description="Mint a special lecture certificate to one student address."
    )
    parser.add_argument("--recipient", help="wallet address")
    parser.add_argument("--alias", help="student alias shown on certificate")
    parser.add_argument(
        "--course-title",
        default="Blockchain Special Lecture",
        help="course title written into the certificate",
    )
    parser.add_argument(
        "--issued-at",
        default=date.today().isoformat(),
        help="label for issue date, default is today's YYYY-MM-DD",
    )
    parser.add_argument(
        "--token-uri",
        default="",
        help="optional metadata URI. leave empty if not using external metadata",
    )
    return parser


def ask_if_empty(value, prompt):
    if value:
        return value.strip()
    return input(prompt).strip()


def main():
    parser = build_parser()
    args = parser.parse_args()

    recipient = ask_if_empty(args.recipient, "Student wallet address: ")
    learner_alias = ask_if_empty(args.alias, "Certificate alias/name: ")
    course_title = ask_if_empty(args.course_title, "Course title: ")
    issued_at = ask_if_empty(args.issued_at, "Issued date label: ")
    token_uri = args.token_uri

    w3 = make_web3()
    account = get_account(w3)
    contract = w3.eth.contract(
        address=get_address("CERTIFICATE_ADDRESS"),
        abi=CERTIFICATE_ABI,
    )

    checksum_recipient = w3.to_checksum_address(recipient)
    tx_hash, receipt = send_contract_call(
        contract.functions.issueCertificate(
            checksum_recipient,
            learner_alias,
            course_title,
            issued_at,
            token_uri,
        ),
        w3,
        account,
        gas=700000,
    )

    token_id = contract.functions.tokenOf(checksum_recipient).call()
    certificate = contract.functions.getCertificate(token_id).call()

    print("tx_hash:", tx_hash)
    print("receipt_status:", int(receipt.status))
    print("token_id:", int(token_id))
    print(
        "certificate:",
        json.dumps(
            {
                "recipient": certificate[0],
                "alias": certificate[1],
                "course_title": certificate[2],
                "issued_at": certificate[3],
                "token_uri": certificate[4],
            },
            ensure_ascii=False,
            indent=2,
        ),
    )
    print("explorer_url:", f"https://sepolia.etherscan.io/tx/{tx_hash}")


if __name__ == "__main__":
    main()
