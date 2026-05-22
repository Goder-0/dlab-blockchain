// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./Owned.sol";

contract ClassCertificate is Owned {
    error EmptyText();
    error AlreadyIssued();
    error TokenDoesNotExist();
    error Soulbound();

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event CertificateIssued(
        uint256 indexed tokenId,
        address indexed recipient,
        string learnerAlias,
        string courseTitle
    );

    string public constant name = "Special Lecture Certificate";
    string public constant symbol = "SLCERT";

    struct CertificateData {
        address recipient;
        string learnerAlias;
        string courseTitle;
        string issuedAtLabel;
        string tokenUri;
    }

    uint256 private _nextTokenId = 1;

    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(address => uint256) private _issuedTokenByAddress;
    mapping(uint256 => CertificateData) private _certificates;

    function supportsInterface(bytes4 interfaceId) external pure returns (bool) {
        return
            interfaceId == 0x01ffc9a7 || // ERC165
            interfaceId == 0x80ac58cd || // ERC721
            interfaceId == 0x5b5e139f; // ERC721Metadata
    }

    function totalSupply() external view returns (uint256) {
        return _nextTokenId - 1;
    }

    function balanceOf(address owner_) external view returns (uint256) {
        if (owner_ == address(0)) revert ZeroAddress();
        return _balances[owner_];
    }

    function ownerOf(uint256 tokenId) public view returns (address) {
        address owner_ = _owners[tokenId];
        if (owner_ == address(0)) revert TokenDoesNotExist();
        return owner_;
    }

    function tokenURI(uint256 tokenId) external view returns (string memory) {
        ownerOf(tokenId);
        return _certificates[tokenId].tokenUri;
    }

    function tokenOf(address recipient) external view returns (uint256) {
        return _issuedTokenByAddress[recipient];
    }

    function getCertificate(uint256 tokenId)
        external
        view
        returns (address, string memory, string memory, string memory, string memory)
    {
        ownerOf(tokenId);
        CertificateData storage item = _certificates[tokenId];
        return (
            item.recipient,
            item.learnerAlias,
            item.courseTitle,
            item.issuedAtLabel,
            item.tokenUri
        );
    }

    function issueCertificate(
        address recipient,
        string calldata learnerAlias,
        string calldata courseTitle,
        string calldata issuedAtLabel,
        string calldata tokenUri_
    ) external onlyOwner returns (uint256) {
        if (recipient == address(0)) revert ZeroAddress();
        if (bytes(learnerAlias).length == 0) revert EmptyText();
        if (bytes(courseTitle).length == 0) revert EmptyText();
        if (_issuedTokenByAddress[recipient] != 0) revert AlreadyIssued();

        uint256 tokenId = _nextTokenId;
        _nextTokenId += 1;

        _owners[tokenId] = recipient;
        _balances[recipient] += 1;
        _issuedTokenByAddress[recipient] = tokenId;
        _certificates[tokenId] = CertificateData({
            recipient: recipient,
            learnerAlias: learnerAlias,
            courseTitle: courseTitle,
            issuedAtLabel: issuedAtLabel,
            tokenUri: tokenUri_
        });

        emit Transfer(address(0), recipient, tokenId);
        emit CertificateIssued(tokenId, recipient, learnerAlias, courseTitle);
        return tokenId;
    }

    function approve(address, uint256) external pure {
        revert Soulbound();
    }

    function setApprovalForAll(address, bool) external pure {
        revert Soulbound();
    }

    function getApproved(uint256 tokenId) external view returns (address) {
        ownerOf(tokenId);
        return address(0);
    }

    function isApprovedForAll(address, address) external pure returns (bool) {
        return false;
    }

    function transferFrom(address, address, uint256) external pure {
        revert Soulbound();
    }

    function safeTransferFrom(address, address, uint256) external pure {
        revert Soulbound();
    }

    function safeTransferFrom(address, address, uint256, bytes calldata) external pure {
        revert Soulbound();
    }
}
