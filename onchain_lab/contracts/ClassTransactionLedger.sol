// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./Owned.sol";

contract ClassTransactionLedger is Owned {
    error EmptyText();
    error DuplicateAccount();
    error UnknownAccount();
    error InvalidLength();
    error InvalidAmount();
    error SameSenderReceiver();
    error InsufficientBalance();
    error ReceiverCapExceeded();

    uint256 public constant DEFAULT_STUDENT_BALANCE = 20;
    uint256 public constant DEFAULT_MAX_BALANCE = 60;
    uint256 public constant DEFAULT_TX_FEE = 1;

    struct AccountState {
        string label;
        uint256 balance;
        bool exists;
    }

    struct LedgerBlock {
        uint256 index;
        uint256 txStart;
        uint256 txCount;
        uint256 rejectedCount;
        string note;
        uint256 timestamp;
    }

    struct LedgerTx {
        uint256 blockIndex;
        string sender;
        string receiver;
        uint256 amount;
        uint256 fee;
        string studentLabel;
        uint256 timestamp;
    }

    struct ClassroomTxInput {
        string sender;
        string receiver;
        uint256 amount;
        string studentLabel;
    }

    mapping(bytes32 => AccountState) private accounts;
    string[] private accountLabels;
    LedgerBlock[] private blocks;
    LedgerTx[] private txs;

    event AccountAdded(string label, uint256 initialBalance);
    event ClassroomBlockRecorded(
        uint256 indexed index,
        uint256 txCount,
        uint256 rejectedCount,
        string note,
        uint256 timestamp
    );
    event ClassroomTxRecorded(
        uint256 indexed blockIndex,
        string sender,
        string receiver,
        uint256 amount,
        uint256 fee,
        string studentLabel
    );

    constructor() {
        _registerAccount("atlas-01", DEFAULT_STUDENT_BALANCE);
        _registerAccount("blaze-02", DEFAULT_STUDENT_BALANCE);
        _registerAccount("comet-03", DEFAULT_STUDENT_BALANCE);
        _registerAccount("drift-04", DEFAULT_STUDENT_BALANCE);
        _registerAccount("ember-05", DEFAULT_STUDENT_BALANCE);
        _registerAccount("frost-06", DEFAULT_STUDENT_BALANCE);
        _registerAccount("glint-07", DEFAULT_STUDENT_BALANCE);
        _registerAccount("harbor-08", DEFAULT_STUDENT_BALANCE);
        _registerAccount("ion-09", DEFAULT_STUDENT_BALANCE);
        _registerAccount("jade-10", DEFAULT_STUDENT_BALANCE);
    }

    function addAccount(string calldata label, uint256 initialBalance) external onlyOwner {
        if (bytes(label).length == 0) revert EmptyText();
        if (initialBalance == 0 || initialBalance > DEFAULT_MAX_BALANCE) revert InvalidAmount();

        _registerAccount(label, initialBalance);
        emit AccountAdded(label, initialBalance);
    }

    function recordClassBlock(
        ClassroomTxInput[] calldata entries,
        uint256 rejectedCount,
        string calldata note
    ) external onlyOwner {
        uint256 txCount = entries.length;
        uint256 newBlockIndex = blocks.length;
        uint256 txStart = txs.length;
        uint256 timestamp = block.timestamp;

        for (uint256 i = 0; i < txCount; i++) {
            _recordSingleTx(entries[i], newBlockIndex, timestamp);
        }

        blocks.push(
            LedgerBlock({
                index: newBlockIndex,
                txStart: txStart,
                txCount: txCount,
                rejectedCount: rejectedCount,
                note: note,
                timestamp: timestamp
            })
        );

        emit ClassroomBlockRecorded(newBlockIndex, txCount, rejectedCount, note, timestamp);
    }

    function _recordSingleTx(
        ClassroomTxInput calldata entry,
        uint256 blockIndex,
        uint256 timestamp
    ) internal {
        bytes32 senderKey = _accountKey(entry.sender);
        bytes32 receiverKey = _accountKey(entry.receiver);

        if (!accounts[senderKey].exists || !accounts[receiverKey].exists) revert UnknownAccount();
        if (keccak256(bytes(entry.sender)) == keccak256(bytes(entry.receiver))) {
            revert SameSenderReceiver();
        }
        if (entry.amount == 0) revert InvalidAmount();
        if (accounts[senderKey].balance < entry.amount + DEFAULT_TX_FEE) {
            revert InsufficientBalance();
        }
        if (accounts[receiverKey].balance + entry.amount > DEFAULT_MAX_BALANCE) {
            revert ReceiverCapExceeded();
        }

        accounts[senderKey].balance -= entry.amount + DEFAULT_TX_FEE;
        accounts[receiverKey].balance += entry.amount;

        txs.push(
            LedgerTx({
                blockIndex: blockIndex,
                sender: entry.sender,
                receiver: entry.receiver,
                amount: entry.amount,
                fee: DEFAULT_TX_FEE,
                studentLabel: entry.studentLabel,
                timestamp: timestamp
            })
        );

        emit ClassroomTxRecorded(
            blockIndex,
            entry.sender,
            entry.receiver,
            entry.amount,
            DEFAULT_TX_FEE,
            entry.studentLabel
        );
    }

    function accountCount() external view returns (uint256) {
        return accountLabels.length;
    }

    function getAccount(uint256 index) external view returns (string memory, uint256) {
        string memory label = accountLabels[index];
        AccountState storage state = accounts[_accountKey(label)];
        return (state.label, state.balance);
    }

    function getAccountByLabel(string calldata label) external view returns (string memory, uint256) {
        AccountState storage state = accounts[_accountKey(label)];
        if (!state.exists) revert UnknownAccount();
        return (state.label, state.balance);
    }

    function blockCount() external view returns (uint256) {
        return blocks.length;
    }

    function getBlock(uint256 index)
        external
        view
        returns (uint256, uint256, uint256, uint256, string memory, uint256)
    {
        LedgerBlock memory item = blocks[index];
        return (
            item.index,
            item.txStart,
            item.txCount,
            item.rejectedCount,
            item.note,
            item.timestamp
        );
    }

    function txCount() external view returns (uint256) {
        return txs.length;
    }

    function getTx(uint256 index)
        external
        view
        returns (uint256, string memory, string memory, uint256, uint256, string memory, uint256)
    {
        LedgerTx memory item = txs[index];
        return (
            item.blockIndex,
            item.sender,
            item.receiver,
            item.amount,
            item.fee,
            item.studentLabel,
            item.timestamp
        );
    }

    function _registerAccount(string memory label, uint256 initialBalance) internal {
        bytes32 key = _accountKey(label);
        if (accounts[key].exists) revert DuplicateAccount();

        accounts[key] = AccountState({label: label, balance: initialBalance, exists: true});
        accountLabels.push(label);
    }

    function _accountKey(string memory label) internal pure returns (bytes32) {
        return keccak256(bytes(label));
    }
}
