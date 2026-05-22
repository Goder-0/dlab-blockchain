// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleClassChain {
    struct BlockInfo {
        uint256 index;
        bytes32 prevHash;
        bytes32 blockHash;
        string note;
        uint256 timestamp;
    }

    BlockInfo[] public chain;

    event BlockAdded(
        uint256 indexed index,
        bytes32 blockHash,
        bytes32 prevHash,
        string note,
        uint256 timestamp
    );

    constructor() {
        chain.push(
            BlockInfo({
                index: 0,
                prevHash: bytes32(0),
                blockHash: keccak256(abi.encodePacked("GENESIS")),
                note: "GENESIS",
                timestamp: block.timestamp
            })
        );
    }

    function addBlock(bytes32 blockHash, string calldata note) external {
        bytes32 prev = chain[chain.length - 1].blockHash;
        uint256 newIndex = chain.length;
        chain.push(
            BlockInfo({
                index: newIndex,
                prevHash: prev,
                blockHash: blockHash,
                note: note,
                timestamp: block.timestamp
            })
        );
        emit BlockAdded(newIndex, blockHash, prev, note, block.timestamp);
    }

    function length() external view returns (uint256) {
        return chain.length;
    }

    function getBlock(uint256 i)
        external
        view
        returns (uint256, bytes32, bytes32, string memory, uint256)
    {
        BlockInfo memory b = chain[i];
        return (b.index, b.prevHash, b.blockHash, b.note, b.timestamp);
    }
}
