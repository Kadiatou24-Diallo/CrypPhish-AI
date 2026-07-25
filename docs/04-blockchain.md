# Blockchain Module

## Overview

The Blockchain module enhances the security of the phishing email detection system by storing the hash and metadata of legitimate emails on the Ethereum blockchain.

This approach guarantees data integrity, immutability, traceability, and non-repudiation.

---

## Blockchain Workflow

The blockchain process follows these steps:

1. Receive a legitimate email.
2. Generate a SHA-256 hash.
3. Collect the email metadata.
4. Execute the smart contract.
5. Store the record on the Ethereum blockchain.
6. Verify transaction success.

---

## Blockchain Components

### Ethereum

Ethereum provides the decentralized blockchain network used to store verified email records.

### Ganache

Ganache is used as the local Ethereum test network during development and testing.

### Smart Contract

The Solidity smart contract records:

- Email Hash
- Sender
- Subject
- Timestamp
- AI Prediction

---

## Smart Contract Functions

The smart contract performs the following tasks:

- Store verified email records.
- Prevent modification of stored information.
- Retrieve stored email records.
- Ensure transparency and traceability.

---

## SHA-256 Hashing

Before storing an email on the blockchain, the system generates a SHA-256 cryptographic hash.

Instead of storing the complete email, only its hash and metadata are recorded.

This approach protects user privacy while maintaining data integrity.

---

## Blockchain Security Benefits

The integration of Ethereum blockchain provides:

- Data Integrity
- Immutability
- Transparency
- Traceability
- Secure Verification
- Non-Repudiation

---

## Integration with AI

Only emails classified as **Legitimate** by the Machine Learning model are forwarded to the blockchain module.

Phishing emails are flagged and quarantined without being recorded on the blockchain.
