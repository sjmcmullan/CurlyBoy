CREATE TABLE Staff_Contact (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CourseID varchar(7) NOT NULL,
    FirstName varchar(20) NOT NULL,
    LastName varchar(20) NOT NULL,
    Role varchar(20) NOT NULL,
    PhoneNumber varchar(10) NOT NULL,
    Email varchar(100) NOT NULL,
    Office varchar(50) NOT NULL,
    OfficeHours varchar(50) NOT NULL
);