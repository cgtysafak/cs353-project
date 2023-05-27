DROP TABLE IF EXISTS Chat;
DROP TABLE IF EXISTS Application;
DROP TABLE IF EXISTS Blocked;
DROP TABLE IF EXISTS Connection;
DROP TABLE IF EXISTS Notification;
DROP TABLE IF EXISTS Message;
DROP TABLE IF EXISTS Comment;
DROP TABLE IF EXISTS Post;
DROP TABLE IF EXISTS Job;
DROP TABLE IF EXISTS CareerGrade;
DROP TABLE IF EXISTS Education;
DROP TABLE IF EXISTS Employment;
DROP TABLE IF EXISTS Company;
DROP TABLE IF EXISTS Experience;
DROP TABLE IF EXISTS Report;
DROP TABLE IF EXISTS CareerExpert;
DROP TABLE IF EXISTS Recruiter;
DROP TABLE IF EXISTS RegularUser;
DROP TABLE IF EXISTS NonAdmin;
DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS User;


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
    FOREIGN KEY(user_id) REFERENCES NonAdmin(user_id)
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
    title VARCHAR(100),
    description TEXT,
    start_date DATETIME NOT NULL,
    end_date DATETIME,
    FOREIGN KEY(user_id) REFERENCES NonAdmin(user_id)
);

CREATE TABLE Company( 
    company_id INTEGER PRIMARY KEY,
    location VARCHAR(255),
    description VARCHAR(1023),
    name VARCHAR(255) NOT NULL
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
    FOREIGN KEY (company_id) REFERENCES Company(company_id),
    FOREIGN KEY (recruiter_id) REFERENCES Recruiter(user_id)
);

CREATE TABLE Post(
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(100),
    content TEXT,
    date DATETIME,
    FOREIGN KEY (user_id) REFERENCES NonAdmin(user_id)
);

CREATE TABLE Comment (
    comment_id INTEGER,
    post_id INTEGER,
    user_id INTEGER NOT NULL,
    content TEXT,
    date DATETIME,
    PRIMARY KEY (comment_id, post_id),
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
    FOREIGN KEY(job_id) REFERENCES Company(company_id)
);

CREATE TABLE Chat( 
    user_id1 INTEGER NOT NULL,
    user_id2 INTEGER NOT NULL,
    PRIMARY KEY(user_id1, user_id2),
    FOREIGN KEY(user_id1) REFERENCES NonAdmin(user_id),
    FOREIGN KEY(user_id2) REFERENCES NonAdmin(user_id)
);

INSERT INTO User(full_name, username, password, email_address, dp_url, date_of_registration, user_type)
VALUES
    ('John Doe', 'johndoe', 'password123', 'johndoe@example.com', 'https://example.com/johndoe.jpg', '2023-05-13 10:30:00', 'RegularUser'),
    ('Jane Smith', 'janesmith', 'letmein', 'janesmith@example.com', 'https://example.com/janesmith.jpg', '2023-05-14 15:45:00', 'Recruiter'),
    ('Robert Johnson', 'robjohnson', 'secret123', 'robjohnson@example.com', NULL, '2023-05-15 09:00:00', 'RegularUser'),
    ('Adison Miner', 'admin', 'admin123', 'admin@example.com', NULL, '2023-05-24 20:15:00', 'Admin'),
    ('Jake Ray', 'jakeray', 'hello987', 'jaker@example.com', 'https://example.com/jaker.jpg', '2023-01-09 22:33:44', 'Career Expert');

INSERT INTO Admin(user_id)
VALUES
    (4);

INSERT INTO NonAdmin(user_id, birth_date, profession, skills)
VALUES
    (1, '1985-07-17', 'Junior Programmer', 'Python, Java, C#, Ruby, Swift'),
    (2, '1974-11-28', 'Human Resources', 'Finance, Business' ),
    (3, '2000-06-09', 'Professor', 'Machine Engineering, Statistics'),
    (5, '1989-03-13', 'Career Expert', 'Career Advisor');

INSERT INTO RegularUser(user_id, portfolio_url, avg_career_grd)
VALUES
    (1, 'https://example.com/janesmith.pdf', 97.89),
    (3, 'https://example.com/robj.pdf', 85.324 );

INSERT INTO Recruiter(user_id)
VALUES
    (2);

INSERT INTO CareerExpert(user_id)
VALUES
    (5);

INSERT INTO Report(report_id, report_url, start_date, location, job_type, user_type, creator_id)
VALUES 
    (1, 'https://example.com/report.pdf', '2023-02-25 14:32:56', 'Ankara', 'Part-Time', 'Regular User', 4);

INSERT INTO Experience(experience_id, user_id, description, start_date, end_date)
VALUES
    (1, 1, 'Job at Microsoft', '2019-08-30', '2022-04-04'),
    (2, 2, 'Job at Apple', '2022-07-25', '2023-02-01'),
    (3, 2, 'Job at Google', '2016-04-29', '2023-05-06'),
    (4, 3, 'Internship at Intel', '2022-09-18', '2022-10-25'),
    (5, 5, 'Job at Apple', '2005-01-13', '2018-03-23'), 
    (6, 1, 'University', '2012-09-12', '2016-06-24'),
    (7, 2, 'University', '2008-07-27', '2012-05-05'),
    (8, 3, 'University', '2018-08-29', '2022-06-14');

INSERT INTO Company(company_id, location, description, name)
VALUES
    (1, 'Washington', 'Microsoft is a multinational technology corporation.', 'Microsoft Corporation'),
    (2, 'Cupertino', 'Apple produces consumer electronics and software.', 'Apple Inc.'),
    (3, 'California', 'Google is known for internet-related products.', 'Google LLC'),
    (4, 'California', 'Intel manufactures computer processors and hardware.', 'Intel');

INSERT INTO Employment(experience_id, company_id, profession)
VALUES
    (1, 1, 'Junior Software Developer'),
    (2, 2, 'Project Manager'),
    (3, 3, 'Data Analyst'),
    (4, 4, 'Senior Software Developer'),
    (5, 2, 'Software Engineer');

INSERT INTO Education(experience_id, school_name, degree, department, cgpa)
VALUES
    (6, 'Bilkent University', "Bachelor's Degree", 'Electrical-Electronics Engineering', 2.92),
    (7, 'Harvard University', "Bachelor's Degree", 'Software Engineering', 3.01),
    (8, 'Oxford University', "Bachelor's Degree", 'Computer Science', 2.89);

