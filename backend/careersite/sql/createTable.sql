

DROP TABLE if EXISTS User;
DROP TABLE if EXISTS Admin;
DROP TABLE if EXISTS NonAdmin;
DROP TABLE if EXISTS RegularUser;
DROP TABLE if EXISTS Recruiter;
DROP TABLE if EXISTS CareerExpert;
DROP TABLE if EXISTS Report;
DROP TABLE if EXISTS Experience;
DROP TABLE if EXISTS Employment;
DROP TABLE if EXISTS Education;
DROP TABLE if EXISTS CareerGrade;
DROP TABLE if EXISTS Company;
DROP TABLE if EXISTS Job;
DROP TABLE if EXISTS Post;
DROP TABLE if EXISTS Comment;
DROP TABLE if EXISTS Message;
DROP TABLE if EXISTS Notification;
DROP TABLE if EXISTS Connection;
DROP TABLE if EXISTS Blocked;
DROP TABLE if EXISTS Application;
DROP TABLE if EXISTS Chat;




CREATE TABLE User(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(50) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100),
    email_address VARCHAR(100) UNIQUE NOT NULL,
    dp_url VARCHAR(255),
    date_of_registration DATETIME,
    user_type VARCHAR(30)
);

CREATE TABLE Admin(
    user_id INTEGER PRIMARY KEY,
    FOREIGN KEY(user_id) REFERENCES User(user_id)
);

CREATE TABLE NonAdmin(
    user_id INTEGER PRIMARY KEY,
    birth_date DATETIME,
    profession VARCHAR(100),
    skills VARCHAR(1023),
    FOREIGN KEY(user_id) REFERENCES User(user_id)
);

CREATE TABLE RegularUser(
    user_id INTEGER PRIMARY KEY,
    portfolio_url VARCHAR(255),
    avg_career_grd REAL,
    FOREIGN KEY(user_id) REFERENCES NonAdmin(user_id)
);

CREATE TABLE Recruiter(
    user_id INTEGER PRIMARY KEY,
    FOREIGN KEY(user_id) REFERENCES NonAdmin(user_id)
);

CREATE TABLE CareerExpert(
    user_id INTEGER PRIMARY KEY,
    FOREIGN KEY(user_id) REFERENCES RegularUser(user_id)
);

CREATE TABLE Report(
    report_id INTEGER PRIMARY KEY,
    report_url VARCHAR(255) NOT NULL,
    start_date DATETIME,
    location VARCHAR(100),
    job_type VARCHAR(100),
    user_type VARCHAR(100),
    creator_id INTEGER NOT NULL,
    FOREIGN KEY(creator_id) REFERENCES Admin(user_id)
);

CREATE TABLE Experience(
    experience_id INTEGER PRIMARY KEY,
    user_id INT NOT NULL,
    description TEXT,
    start_date DATETIME NOT NULL,
    end_date DATETIME,
    FOREIGN KEY(user_id) REFERENCES NonAdmin(user_id)
);

CREATE TABLE Employment(
    experience_id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    profession VARCHAR(100),
    FOREIGN KEY(experience_id) REFERENCES Experience(experience_id),
    FOREIGN KEY(company_id) REFERENCES Company(company_id)
);

CREATE TABLE Education(
    experience_id INTEGER PRIMARY KEY,
    school_name VARCHAR(255) NOT NULL,
    degree VARCHAR(255),
    department VARCHAR(255),
    cgpa NUMERIC(3, 2) CHECK (cgpa BETWEEN 0.00 AND 4.00),
    FOREIGN KEY (experience_id) REFERENCES Experience(experience_id)
);

CREATE TABLE CareerGrade( 
    grade_id INTEGER,
    user_id INTEGER NOT NULL,
    expert_id INTEGER NOT NULL,
    grade INTEGER NOT NULL,
    feedback_text TEXT,
    PRIMARY KEY(grade_id, user_id, expert_id),
    FOREIGN KEY (user_id) REFERENCES NonAdmin(user_id),
    FOREIGN KEY (expert_id) REFERENCES CareerExpert(user_id)
);

CREATE TRIGGER insert_careergrade_id AFTER INSERT ON CareerGrade
BEGIN
	UPDATE CareerGrade SET grade_id = (SELECT MAX(grade_id) FROM CareerGrade WHERE user_id = NEW.user_id AND expert_id = NEW.expert_id);
END;

CREATE TABLE Company( 
    company_id INTEGER PRIMARY KEY,
    location VARCHAR(255),
    description VARCHAR(1023),
    name VARCHAR(255) NOT NULL
);	

CREATE TABLE Job(
    company_id INTEGER NOT NULL,
    recruiter_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    title VARCHAR(255),
    due_date DATETIME,
    profession VARCHAR(255),
    location VARCHAR(255),
    job_requirements VARCHAR(1023),
    description VARCHAR(1023),
    PRIMARY KEY (company_id, job_id),
    FOREIGN KEY (company_id) REFERENCES Company (company_id),
    FOREIGN KEY (recruiter_id) REFERENCES Recruiter(user_id)
);

CREATE TABLE Post(
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content TEXT,
    date DATETIME,
    FOREIGN KEY (user_id) REFERENCES NonAdmin(user_id)
);

CREATE TABLE Comment(
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    content TEXT,
    date DATETIME,
    FOREIGN KEY (user_id) REFERENCES NonAdmin(user_id),
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
);

CREATE TABLE Message( 
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME,
    FOREIGN KEY (sender_id, receiver_id) REFERENCES Chat(user_id1, user_id2)
);

CREATE TABLE Notification(
    notification_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    notification_type VARCHAR(100),
    content TEXT,
    timestamp DATETIME,
    PRIMARY KEY(notification_id, user_id),
    FOREIGN KEY (user_id) REFERENCES NonAdmin(user_id)
);

CREATE TABLE Connection(
    user_id1 INTEGER NOT NULL,
    user_id2 INTEGER NOT NULL,
    status TEXT CHECK (status IN ('rejected', 'approved', 'waiting') ) NOT NULL DEFAULT 'waiting',
    PRIMARY KEY(user_id1, user_id2),
    FOREIGN KEY (user_id1) REFERENCES NonAdmin(user_id),
    FOREIGN KEY (user_id2) REFERENCES NonAdmin(user_id)
);

CREATE TABLE Blocked(
    user_id1 INTEGER NOT NULL,
    user_id2 INTEGER NOT NULL,
    PRIMARY KEY(user_id1, user_id2),
    FOREIGN KEY (user_id1) REFERENCES NonAdmin(user_id),
    FOREIGN KEY (user_id2) REFERENCES NonAdmin(user_id)
);


CREATE TABLE Application( 
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    date DATETIME,
    personal_info TEXT,
    cv_url VARCHAR(255),
    PRIMARY KEY(user_id, job_id),
    FOREIGN KEY(user_id) REFERENCES NonAdmin(user_id),
    FOREIGN KEY(job_id) REFERENCES Company(job_id)
);

CREATE TABLE Chat( 
    user_id1 INTEGER NOT NULL,
    user_id2 INTEGER NOT NULL,
    PRIMARY KEY(user_id1, user_id2),
    FOREIGN KEY(user_id1) REFERENCES NonAdmin(user_id),
    FOREIGN KEY(user_id2) REFERENCES NonAdmin(user_id)
);


INSERT INTO User (full_name, username, password, email_address, dp_url, date_of_registration, user_type)
VALUES
    ('John Doe', 'johndoe', 'password123', 'johndoe@example.com', 'https://example.com/johndoe.jpg', '2023-05-13 10:30:00', 'RegularUser'),
    ('Jane Smith', 'janesmith', 'letmein', 'janesmith@example.com', 'https://example.com/janesmith.jpg', '2023-05-14 15:45:00', 'Recruiter'),
    ('Robert Johnson', 'robjohnson', 'secret123', 'robjohnson@example.com', NULL, '2023-05-15 09:00:00', 'RegularUser');








	






