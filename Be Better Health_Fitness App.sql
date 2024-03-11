CREATE TABLE persoInfo(
    user_id VARCHAR(15) PRIMARY KEY,
    username VARCHAR(10),
    pass VARCHAR(10),
    name VARCHAR(15),
    age INT,
    gender VARCHAR(10),
    height INT,
    weight INT
);

CREATE TABLE health_data (
    health_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(15),
    activity_date VARCHAR(10),
    TotalSteps INT,
    TotalDistance FLOAT,
    VeryActiveMinutes INT,
    FairlyActiveMinutes INT,
    LightlyActiveMinutes INT,
    SedentaryMinutes INT,
    Calories INT,
    TotalTimeAsleep INT,
    TotalTimeInBed INT,

    FOREIGN KEY (user_id) REFERENCES persoInfo(user_id)
);

CREATE TABLE injury_history (
    injury_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(15),
    injury_date DATE,
    injury_description TEXT,
    -- Other fields related to injury history
    FOREIGN KEY (user_id) REFERENCES persoInfo(user_id)
);

#how to drop a row
DELETE FROM health_data
WHERE injury_id = 5;

#visualize a table
select * from health_data;

#delete a table
DROP TABLE health_data;

#add column in table
ALTER TABLE injury_history
ADD COLUMN recovery TEXT;