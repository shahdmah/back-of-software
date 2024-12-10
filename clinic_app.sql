-- إنشاء قاعدة بيانات جديدة
CREATE DATABASE IF NOT EXISTS clinic_app;
USE clinic_app;

-- إنشاء جدول المستخدمين
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'doctor') DEFAULT 'student' -- تحديد نوع المستخدم (طالب أو طبيب)
);

-- إنشاء جدول المواعيد
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    day DATE NOT NULL,
    time TIME NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);

-- إدخال بيانات تجريبية للمستخدمين
INSERT INTO users (username, email, password, role)
VALUES
('Ahmed Ali', 'ahmed@example.com', 'password1', 'student'),
('Ali Hassan', 'ali@example.com', 'password2', 'student'),
('Omar Fayed', 'omar@example.com', 'password3', 'student'),
('Shahd Salama', 'shahd@example.com', 'password4', 'student'),
('Yousef Khaled', 'yousef@example.com', 'password5', 'student'),
('Dr. Tamer Youssef', 'tamer@example.com', 'password6', 'doctor');

-- إدخال بيانات تجريبية للمواعيد
INSERT INTO appointments (student_id, doctor_name, day, time, status)
VALUES
(1, 'Dr. Tamer', '2024-11-25', '10:00:00', 'pending'),
(2, 'Dr. Tamer', '2024-11-26', '12:00:00', 'approved'),
(3, 'Dr. Tamer', '2024-11-27', '14:00:00', 'rejected'),
(4, 'Dr. Tamer', '2024-11-28', '11:00:00', 'pending'),
(5, 'Dr. Tamer', '2024-11-29', '13:00:00', 'pending');
DROP DATABASE IF EXISTS clinic;
