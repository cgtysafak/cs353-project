DROP TABLE IF EXISTS User;

CREATE TABLE User(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(50) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100),
    email_address VARCHAR(100) UNIQUE NOT NULL,
    dp_url VARCHAR(255),
    date_of_registration DATETIME
);


INSERT INTO User (full_name, username, password, email_address, dp_url, date_of_registration)
VALUES
    ('John Doe', 'johndoe', 'password123', 'johndoe@example.com', 'https://example.com/johndoe.jpg', '2023-05-13 10:30:00'),
    ('Jane Smith', 'janesmith', 'letmein', 'janesmith@example.com', 'https://example.com/janesmith.jpg', '2023-05-14 15:45:00'),
    ('Robert Johnson', 'robjohnson', 'secret123', 'robjohnson@example.com', NULL, '2023-05-15 09:00:00');








	






