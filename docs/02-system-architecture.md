# System Architecture

## Overview

CrypPhish-AI integrates Artificial Intelligence and Ethereum blockchain to provide an intelligent and secure phishing email detection framework.

The system combines Machine Learning for email classification with blockchain technology to ensure the integrity and traceability of legitimate email records.

---

## System Architecture Diagram

![System Architecture](../assets/architecture/system-architecture.png)

---

## Architecture Workflow

The framework operates through the following stages:

### 1. Email Reception

The system receives an incoming email from the user.

---

### 2. Machine Learning Analysis

The email is processed using trained Machine Learning models to extract features and classify the message.

---

### 3. Email Classification

The AI model classifies the email into one of two categories:

- Legitimate
- Phishing

---

### 4. Phishing Detection

If the email is classified as phishing:

- The email is flagged.
- The user is warned.
- The email can be quarantined.

---

### 5. Blockchain Logging

If the email is legitimate:

- SHA-256 generates the email hash.
- Metadata is recorded.
- The smart contract stores the information on the Ethereum blockchain.

---

### 6. Secure Communication

The blockchain guarantees:

- Integrity
- Immutability
- Traceability
- Non-repudiation

---

## Technologies Used

| Component | Technology |
|-----------|------------|
| Artificial Intelligence | Machine Learning |
| Programming Language | Python |
| Web Framework | Streamlit |
| Blockchain | Ethereum |
| Smart Contract | Solidity |
| Development Network | Ganache |
| Hashing | SHA-256 |
