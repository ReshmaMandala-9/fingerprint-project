CREATE DATABASE fingerprint_bloodgroup_db;
USE fingerprint_bloodgroup_db;

CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    role VARCHAR(20)
);

CREATE TABLE fingerprint (
    fingerprint_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    image_path VARCHAR(255),
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE model (
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(100),
    accuracy FLOAT,
    training_date DATE
);

CREATE TABLE prediction (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    fingerprint_id INT,
    model_id INT,
    predicted_blood_group VARCHAR(5),
    confidence_score FLOAT,
    prediction_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fingerprint_id) REFERENCES fingerprint(fingerprint_id),
    FOREIGN KEY (model_id) REFERENCES model(model_id)
);
