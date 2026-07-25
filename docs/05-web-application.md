# Web Application

## Overview

CrypPhish-AI provides an interactive web application developed using Streamlit.

The application allows users to submit an email for phishing analysis and securely records legitimate email information on the Ethereum blockchain.

---

## Main Features

The web application provides the following functionalities:

- Email submission
- AI-based phishing prediction
- Prediction confidence display
- SHA-256 hash generation
- Blockchain transaction execution
- Transaction confirmation
- User-friendly interface

---

## Application Workflow

The web application follows these steps:

1. User enters an email.
2. The application preprocesses the email.
3. The Machine Learning model predicts whether the email is Legitimate or Phishing.
4. The prediction result is displayed.
5. If the email is legitimate, its metadata and SHA-256 hash are stored on the Ethereum blockchain.
6. The transaction result is displayed to the user.

---

## User Interface

The Streamlit interface consists of:

- Email input area
- Prediction button
- Prediction result
- Confidence score
- Blockchain transaction information
- Transaction status

---

## Technologies Used

| Component | Technology |
|-----------|------------|
| Web Framework | Streamlit |
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| Blockchain | Ethereum |
| Smart Contract | Solidity |
| Web3 Library | Web3.py |

---

## Integration

The web application connects the following modules:

- Machine Learning Model
- Blockchain Module
- Smart Contract
- Ethereum Network
