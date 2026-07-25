# Machine Learning Module

## Overview

The Machine Learning module is responsible for detecting phishing emails by analyzing the email content and predicting whether the message is **Legitimate** or **Phishing**.

The trained model serves as the core intelligence of the CrypPhish-AI framework.

---

## Machine Learning Workflow

The Machine Learning pipeline consists of the following stages:

1. Dataset Collection
2. Data Preprocessing
3. Feature Extraction
4. Model Training
5. Model Evaluation
6. Model Selection
7. Prediction

---

## Dataset

The phishing email detection model was trained using publicly available email datasets containing both legitimate and phishing emails.

The datasets were cleaned and prepared before training.

---

## Data Preprocessing

The preprocessing stage includes:

- Text cleaning
- Lowercase conversion
- Removal of punctuation
- Stop-word removal
- Tokenization
- Feature extraction

---

## Machine Learning Algorithms

The following algorithms were evaluated:

- Logistic Regression
- Random Forest
- Support Vector Machine (SVM)
- Long Short-Term Memory (LSTM)

---

## Model Evaluation

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC Curve
- Confusion Matrix

---

## Selected Model

The best-performing model was selected and integrated into the Streamlit application for phishing email detection.

The trained model is stored in the `trained-model` directory.

---

## Prediction Process

When a user submits an email:

1. The email content is preprocessed.
2. Features are extracted.
3. The trained model predicts the email category.
4. The prediction confidence is displayed.
5. Legitimate emails proceed to the blockchain module.
