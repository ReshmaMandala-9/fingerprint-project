# Software Requirements Specification (SRS)

## 1. Introduction
The Fingerprint-Based Blood Group Prediction System is a research-oriented application that explores the relationship between fingerprint patterns and blood groups using deep learning techniques.

## 2. Purpose
The purpose of this document is to define the functional and non-functional requirements of the system for academic and research use.

## 3. Scope
The system predicts blood groups using fingerprint images. It is intended for experimental and research purposes and is not a medical diagnostic replacement.

## 4. Overall Description
The system consists of:
- A web-based user interface
- A backend processing layer
- A deep learning model
- A relational database

## 5. Functional Requirements
# Functional Requirements

## FR1: Fingerprint Image Upload
The system shall allow users to upload fingerprint images in standard formats such as JPG and PNG.

## FR2: Image Validation
The system shall validate the uploaded fingerprint image for format and quality before processing.

## FR3: Image Preprocessing
The system shall preprocess fingerprint images to remove noise and enhance ridge patterns.

## FR4: Feature Extraction
The system shall extract relevant fingerprint features automatically using a deep learning model.

## FR5: Blood Group Prediction
The system shall predict the blood group (A, B, AB, O with Rh factor) based on extracted fingerprint features.

## FR6: Result Display
The system shall display the predicted blood group along with a confidence score.

## FR7: Data Storage
The system shall store fingerprint metadata and prediction results for analysis and research purposes.
.

## 6. Non-Functional Requirements
# Non-Functional Requirements

## NFR1: Accuracy
The system should achieve high prediction accuracy based on the quality of the dataset.

## NFR2: Performance
Prediction results should be generated within 2 seconds after image submission.

## NFR3: Scalability
The system should be designed to support future expansion with larger datasets.

## NFR4: Security
Fingerprint data should be handled securely to prevent unauthorized access.

## NFR5: Usability
The user interface should be simple and intuitive for non-technical users.

## NFR6: Reliability
The system should produce consistent predictions for similar fingerprint inputs.

## NFR7: Research Extensibility
The system should support experimentation with different models and datasets for research purposes.

## 7. System Architecture
User → Frontend → Backend API → Deep Learning Model → Database

## 8. Assumptions and Dependencies
- Availability of fingerprint datasets
- Proper image quality
- Trained deep learning model

## 9. Limitations
- Prediction accuracy depends on dataset size and quality
- Research-based probabilistic output
