-- Database: Minneapolis_Restaurants

DROP DATABASE "Minneapolis_Restaurants";

CREATE DATABASE "Minneapolis_Restaurants"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	
DROP TABLE YelpData;

CREATE TABLE YelpData (
	Yelp_Index INT PRIMARY KEY NOT NULL,
	YelpID VARCHAR(50),
	Yelp_Name VARCHAR(75),
	Latitude FLOAT(8),
	Longitude FLOAT (8),
	Address VARCHAR (100),
	Rating FLOAT (1),
	Reviews INT
);

SELECT * FROM YelpData;

DROP TABLE GoogleData;

CREATE TABLE GoogleData (
	Yelp_Index INT NOT NULL,
	GooglePlacesID VARCHAR(75) PRIMARY KEY,
	Google_Name VARCHAR(75),
	Latitude FLOAT(8),
	Longitude FLOAT (8),
	Address VARCHAR (125),
	Rating FLOAT (2),
	Reviews INT
);

SELECT * FROM GoogleData;

DROP TABLE InspectionData;

CREATE TABLE InspectionData (
	Record INT NOT NULL,
	BusinessName VARCHAR(50) NOT NULL,
	DateIfInspection DATE,
	FullAddress VARCHAR(50),
	HealthFacilityIDNumber VARCHAR(15),
	InspectionIDNumber INT PRIMARY KEY,
	InspectionScore INT,
	InspectionType VARCHAR(10),
	Latitude FLOAT(8),
	Longitude FLOAT(8)
);

SELECT * FROM InspectionData;




