// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

abstract contract Owned {
    error NotOwner();
    error ZeroAddress();

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    function transferOwnership(address newOwner) external onlyOwner {
        if (newOwner == address(0)) revert ZeroAddress();
        owner = newOwner;
    }
}
