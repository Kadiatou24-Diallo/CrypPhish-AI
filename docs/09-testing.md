# Testing

## Functional Testing

The following components were tested:

- Email preprocessing
- Machine Learning prediction
- Blockchain connection
- Smart contract execution
- Streamlit interface

---

## Test Cases

| Test Case | Expected Result | Observed Result | Status |
|---|---|---|---|
| Legitimate Email Detection | Email classified as safe | Email successfully classified as SAFE | ✅ Passed |
| Safe Email Blockchain Storage | Safe email stored on blockchain | SHA-256 hash and transaction recorded on Ethereum | ✅ Passed |
| Phishing Email Detection | Email flagged as phishing | Email successfully classified as PHISHING | ✅ Passed |
| Phishing Blockchain Protection | Phishing email must not be stored | Phishing email was not stored on blockchain | ✅ Passed |
| Blockchain Connection | Application connects to Ethereum | Blockchain connection successfully established | ✅ Passed |
| Smart Contract Execution | Smart contract transaction executes successfully | Transaction successfully recorded in Ganache | ✅ Passed |
| Email Verification | Stored email can be verified | Email hash successfully checked against blockchain records | ✅ Passed |

---

## Test Outcome

The integrated framework successfully combines Artificial Intelligence and Ethereum blockchain to detect phishing emails and securely record verified email information.

## Test Evidence

The following screenshots provide visual evidence of the main functional tests performed on the CrypPhish AI system.

### Safe Email Classification and Blockchain Storage

A legitimate email was successfully classified as SAFE. The application generated its SHA-256 hash and recorded the corresponding transaction on the Ethereum blockchain.

![Safe Email Test](../screenshots/crypphish-ai-safe-blockchain-result.png)

### Phishing Email Detection

A phishing email was successfully identified by the machine learning model. As designed, the phishing email was flagged and was not stored on the blockchain.

![Phishing Email Test](../screenshots/crypphish-ai-phishing-detection-result.png)

### Ethereum Blockchain Transaction Test

The blockchain integration was validated using Ganache as the local Ethereum network. Successful transactions confirm that the application can interact with the deployed smart contract and record data on the blockchain.

![Ganache Blockchain Blocks](../screenshots/ganache-blockchain-blocks.png)

### Smart Contract Transaction Evidence

A detailed Ganache transaction confirms the successful execution of the deployed smart contract. The transaction contains the transaction hash, sender address, smart contract address, gas consumption, and the block in which the transaction was recorded.

This provides direct evidence that CrypPhish AI successfully communicates with the Ethereum smart contract.

![Smart Contract Transaction](../screenshots/ganache-smart-contract-transaction.png)

### Blockchain Email Verification Test

The email verification functionality was tested to confirm that CrypPhish AI can check whether an email has previously been registered on the blockchain.

The application computes the SHA-256 hash of the submitted email content and compares it with the records stored on the Ethereum blockchain.

![Blockchain Email Verification Test](../screenshots/crypphish-ai-blockchain-verification.png)

## Test Summary

The functional testing demonstrated that the main components of CrypPhish AI operate together as expected.

The testing covered:

- AI-based classification of legitimate and phishing emails
- Blockchain storage of legitimate email records
- Prevention of phishing email storage on the blockchain
- Ethereum smart contract interaction
- Ganache transaction execution
- Blockchain-based email verification functionality

The results demonstrate the successful integration of the machine learning detection component, the web application, and the Ethereum blockchain environment.
