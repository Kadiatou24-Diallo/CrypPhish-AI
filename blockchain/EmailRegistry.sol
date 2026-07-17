
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmailRegistry {

    struct EmailRecord {
        string  emailHash;    // SHA-256 hash of the email body
        string  sender;       // From: field
        string  subject;      // Subject: field
        string  prediction;   // "safe" or "phishing"
        uint256 timestamp;    // Unix timestamp
    }

    EmailRecord[] private emails;

    event EmailStored(
        uint256 indexed id,
        string  emailHash,
        string  prediction,
        uint256 timestamp
    );

    /// @notice Store a new email record
    function storeEmail(
        string memory _emailHash,
        string memory _sender,
        string memory _subject,
        string memory _prediction
    ) public {
        emails.push(EmailRecord({
            emailHash : _emailHash,
            sender    : _sender,
            subject   : _subject,
            prediction: _prediction,
            timestamp : block.timestamp
        }));
        emit EmailStored(emails.length - 1, _emailHash, _prediction, block.timestamp);
    }

    /// @notice Get a stored record by index
    function getEmail(uint256 index) public view returns (
        string memory, string memory, string memory, string memory, uint256
    ) {
        require(index < emails.length, "Index out of bounds");
        EmailRecord storage r = emails[index];
        return (r.emailHash, r.sender, r.subject, r.prediction, r.timestamp);
    }

    /// @notice Total number of stored emails
    function getEmailCount() public view returns (uint256) {
        return emails.length;
    }
}
