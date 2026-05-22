// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./Owned.sol";

contract LocalBlockAnchor is Owned {
    error EmptyText();
    error EmptyHash();

    struct AnchoredBlock {
        uint256 index;
        bytes32 localBlockHash;
        string stepLabel;
        string teamName;
        string note;
        uint256 timestamp;
    }

    AnchoredBlock[] private anchors;

    event BlockAnchored(
        uint256 indexed index,
        bytes32 indexed localBlockHash,
        string stepLabel,
        string teamName,
        string note,
        uint256 timestamp
    );

    function anchorBlock(
        bytes32 localBlockHash,
        string calldata stepLabel,
        string calldata teamName,
        string calldata note
    ) external onlyOwner {
        if (localBlockHash == bytes32(0)) revert EmptyHash();
        if (bytes(stepLabel).length == 0 || bytes(teamName).length == 0) revert EmptyText();

        uint256 newIndex = anchors.length;
        anchors.push(
            AnchoredBlock({
                index: newIndex,
                localBlockHash: localBlockHash,
                stepLabel: stepLabel,
                teamName: teamName,
                note: note,
                timestamp: block.timestamp
            })
        );

        emit BlockAnchored(newIndex, localBlockHash, stepLabel, teamName, note, block.timestamp);
    }

    function length() external view returns (uint256) {
        return anchors.length;
    }

    function getAnchor(uint256 index)
        external
        view
        returns (uint256, bytes32, string memory, string memory, string memory, uint256)
    {
        AnchoredBlock memory item = anchors[index];
        return (
            item.index,
            item.localBlockHash,
            item.stepLabel,
            item.teamName,
            item.note,
            item.timestamp
        );
    }
}
