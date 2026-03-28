📘 Database Design

Project: Fingerprint-Based Blood Group Detection Using Deep Learning

1. Purpose of the Database

The database is used to store fingerprint-related data, user information, prediction results, and experimental metadata. It supports both system functionality and research analysis.

2. Database Type

Database Management System: MySQL 8.x

Database Model: Relational

Storage Engine: InnoDB

Character Encoding: UTF8MB4

3. Entities and Attributes
3.1 User

user_id (Primary Key)

name

age

gender

role (User / Admin / Researcher)

3.2 Fingerprint

fingerprint_id (Primary Key)

user_id (Foreign Key)

image_path

upload_date

3.3 Model

model_id (Primary Key)

model_name

accuracy

training_date

3.4 Prediction

prediction_id (Primary Key)

fingerprint_id (Foreign Key)

model_id (Foreign Key)

predicted_blood_group

confidence_score

prediction_time

4. Relationships

One User can upload multiple Fingerprints

Each Fingerprint produces one Prediction

One Model can generate multiple Predictions

5. ER Diagram Description

The ER diagram illustrates the relationship between User, Fingerprint, Model, and Prediction entities using primary and foreign keys.

(ER diagram image is stored separately in this folder)

6. Research Perspective

This database design supports structured data storage for experiments, reproducibility of results, and comparison of different deep learning models used for blood group prediction.

7. Conclusion

The MySQL-based relational database ensures data consistency, scalability, and suitability for web-based healthcare and research applications.