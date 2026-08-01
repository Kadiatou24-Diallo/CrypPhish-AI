# Datasets

This directory contains the datasets used to train and evaluate the CrypPhish-AI phishing email detection models.

## Dataset Sources

The project was developed using publicly available email datasets, including:

- SpamAssassin Public Corpus
- Enron Email Dataset
- Nigerian Fraud Email Dataset

These datasets contain legitimate emails, phishing emails, spam emails, and fraud-related messages used for machine learning classification.

---

## Dataset Preparation

Before training, the datasets were processed through the following steps:

1. Data cleaning
2. Duplicate removal
3. Missing value handling
4. Label assignment
5. Text preprocessing
6. TF-IDF feature extraction

---

## Dataset Labels

The machine learning models were trained using the following labels:

| Label | Description |
|--------|-------------|
| Safe | Legitimate email |
| Phishing | Malicious or fraudulent email |

---

## Note

Due to dataset licensing restrictions and repository size limitations, the original datasets are not included in this repository.

Researchers can download the datasets from their official sources and reproduce the experiments following the documentation provided in this repository.

---

## Purpose

The datasets were used for:

- Training Machine Learning models
- Model evaluation
- Performance comparison
- Experimental validation
