// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./Owned.sol";

contract ClassGuestbook is Owned {
    error EmptyText();
    error TextTooLong();

    uint256 public constant MAX_AUTHOR_BYTES = 32;
    uint256 public constant MAX_MESSAGE_BYTES = 160;

    struct GuestbookEntry {
        uint256 index;
        string author;
        string message;
        uint256 timestamp;
    }

    GuestbookEntry[] private entries;

    event GuestbookSigned(
        uint256 indexed index,
        string author,
        string message,
        uint256 timestamp
    );

    function sign(string calldata author, string calldata message) external onlyOwner {
        if (bytes(author).length == 0 || bytes(message).length == 0) revert EmptyText();
        if (bytes(author).length > MAX_AUTHOR_BYTES || bytes(message).length > MAX_MESSAGE_BYTES) {
            revert TextTooLong();
        }

        uint256 newIndex = entries.length;
        entries.push(
            GuestbookEntry({
                index: newIndex,
                author: author,
                message: message,
                timestamp: block.timestamp
            })
        );

        emit GuestbookSigned(newIndex, author, message, block.timestamp);
    }

    function length() external view returns (uint256) {
        return entries.length;
    }

    function getEntry(uint256 index)
        external
        view
        returns (uint256, string memory, string memory, uint256)
    {
        GuestbookEntry memory item = entries[index];
        return (item.index, item.author, item.message, item.timestamp);
    }
}
