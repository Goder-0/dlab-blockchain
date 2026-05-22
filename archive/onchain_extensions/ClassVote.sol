// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./Owned.sol";

contract ClassVote is Owned {
    error InvalidOption();
    error PollClosed();
    error AlreadyVoted();
    error EmptyText();
    error EmptyVoterId();
    error TooFewOptions();

    struct PollOption {
        string label;
        uint256 voteCount;
    }

    string public title;
    bool public closed;
    uint256 public totalVotesCast;

    PollOption[] private options;
    mapping(bytes32 => bool) public hasVoted;

    event VoteCast(
        bytes32 indexed voterIdHash,
        uint8 indexed optionIndex,
        string voterLabel,
        uint256 newVoteCount
    );
    event PollClosed(uint256 totalVotesCast);

    constructor(string memory pollTitle, string[] memory optionLabels) {
        if (bytes(pollTitle).length == 0) revert EmptyText();
        if (optionLabels.length < 2) revert TooFewOptions();

        title = pollTitle;

        for (uint256 i = 0; i < optionLabels.length; i++) {
            if (bytes(optionLabels[i]).length == 0) revert EmptyText();
            options.push(PollOption({label: optionLabels[i], voteCount: 0}));
        }
    }

    function castVote(
        uint8 optionIndex,
        bytes32 voterIdHash,
        string calldata voterLabel
    ) external onlyOwner {
        if (closed) revert PollClosed();
        if (optionIndex >= options.length) revert InvalidOption();
        if (voterIdHash == bytes32(0)) revert EmptyVoterId();
        if (hasVoted[voterIdHash]) revert AlreadyVoted();

        hasVoted[voterIdHash] = true;
        options[optionIndex].voteCount += 1;
        totalVotesCast += 1;

        emit VoteCast(voterIdHash, optionIndex, voterLabel, options[optionIndex].voteCount);
    }

    function closePoll() external onlyOwner {
        closed = true;
        emit PollClosed(totalVotesCast);
    }

    function optionCount() external view returns (uint256) {
        return options.length;
    }

    function getOption(uint256 index) external view returns (string memory, uint256) {
        PollOption memory option = options[index];
        return (option.label, option.voteCount);
    }
}
