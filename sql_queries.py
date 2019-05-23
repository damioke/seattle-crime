import os
import sys
import pymysql
from variables import (datawarehouse_name, useforce_tbl, crime_tbl, host, user, password, report_1,
report_2, report_3, report_4, useforce_file, crimes_file)
########################################################################################

# select datawarehouse
dw_use_query = "USE {};".format(datawarehouse_name)

# create crime table query
useforce_tbl_create_query =  '''
CREATE TABLE IF NOT EXISTS {} (
ID VARCHAR(100),
Incident_Num INT,
Incident_Type VARCHAR(100),
Occured_date_time DATETIME,
Precinct VARCHAR(100),
Sector VARCHAR(100),
Beat VARCHAR(100),
Officer_ID VARCHAR(100),
Subject_ID VARCHAR(100),
Subject_Race VARCHAR(100),
Subject_Gender VARCHAR(100),
PRIMARY KEY (ID)
);
'''.format(useforce_tbl)

# create crime table query
crime_tbl_create_query = '''
CREATE TABLE IF NOT EXISTS {} (
Report_Number VARCHAR(100),
Occurred_Date DATE,
Occurred_Time TIME,
Reported_Date DATE,
Reported_Time TIME,
Crime_Subcategory VARCHAR(100),
Primary_Offense_Description VARCHAR(100),
Precinct VARCHAR(100),
Sector VARCHAR(100),
Beat VARCHAR(100),
Neighborhood VARCHAR(100),
PRIMARY KEY (Report_Number)
);
'''.format(crime_tbl)

create_dw_query = [dw_use_query, useforce_tbl_create_query, crime_tbl_create_query]

########################################################################################

# useforce_tbl load query
useforce_tbl_load = '''
LOAD DATA INFILE {} INTO TABLE {}
COLUMNS TERMINATED BY ','
IGNORE 1 LINES
(ID, Incident_Num,Incident_Type,@Occured_date_time,Precinct,Sector,Beat,Officer_ID,Subject_ID,Subject_Race,Subject_Gender)
SET Occured_date_time = STR_TO_DATE(@Occured_date_time,'%m/%d/%Y %h:%i:%s %p');
'''.format(useforce_file, useforce_tbl)

# crime_tbl_load query
crime_tbl_load = '''
LOAD DATA INFILE {} INTO TABLE crimes COLUMNS TERMINATED BY ',' LINES TERMINATED by '\\n'
IGNORE 1 LINES (Report_Number,@Occurred_Date,@Occurred_Time,@Reported_Date,@Reported_Time,Crime_Subcategory,
Primary_Offense_Description,Precinct,Sector,Beat,Neighborhood)
SET Occurred_Date = STR_TO_DATE(@Occurred_Date,'%m/%d/%Y'),
Reported_Date = STR_TO_DATE(@Reported_Date,'%m/%d/%Y'),
Occurred_Time = STR_TO_DATE(LPAD(@Occurred_Time,4,0),'%H%i'),
Reported_Time = STR_TO_DATE(LPAD(@Reported_Time,4,0),'%H%i');
'''.format(crimes_file, crime_tbl)

load_queries = [useforce_tbl_load, crime_tbl_load]

########################################################################################

query_1 = '''
(SELECT  "Crime Subcategory", "Primary Offense Description", "Occured Date", "Occured Time", "Occurences")
UNION (SELECT Crime_Subcategory, Primary_Offense_Description, Occurred_Date, Occurred_Time, COUNT(*) as Count
FROM crimes
GROUP BY Occurred_Date, Occurred_Time
ORDER BY Occurred_Date DESC
INTO OUTFILE {} 
FIELDS ENCLOSED BY '"' 
TERMINATED BY ',' 
ESCAPED BY '"' 
LINES TERMINATED BY '\\r\\n');
'''.format(report_1)


query_2 = '''
(SELECT  "Crime Subcategory", "Primary Offense Description", "Occured Date", "Occured Time", "Precinct Sector", "Occurences")
UNION (SELECT Crime_Subcategory, Primary_Offense_Description,Occurred_Date, Occurred_Time, CONCAT(Precinct, "-", Sector) as Precinct_Sector,
COUNT(*) as Count
FROM crimes
GROUP BY Occurred_Date, Occurred_Time, Precinct_Sector
ORDER BY Occurred_Date DESC
INTO OUTFILE {} 
FIELDS ENCLOSED BY '"' 
TERMINATED BY ',' 
ESCAPED BY '"' 
LINES TERMINATED BY '\\r\\n');
'''.format(report_2)

query_3 = '''
(SELECT  "Crime Subcategory", "Primary Offense Description", "Occured Time", "Precinct", "Occurences")
UNION (SELECT Crime_Subcategory, Primary_Offense_Description,Occurred_Time, Precinct, COUNT(*) as Count
FROM crimes
GROUP BY Occurred_Time, Precinct
ORDER BY Occurred_Time DESC
INTO OUTFILE {} 
FIELDS ENCLOSED BY '"' 
TERMINATED BY ',' 
ESCAPED BY '"' 
LINES TERMINATED BY '\\r\\n');
'''.format(report_3)

query_4 = '''
(SELECT  "Incident Type", "Precinct Sector", "Precinct", "Date",  "Time", "Occured Date Time", "Count")
UNION (SELECT  Incident_Type, CONCAT(Precinct, "-", Sector) as Precinct_Sector, Precinct, CAST(Occured_date_time as date) as Date, CAST(Occured_date_time as time) as Time, Occured_date_time,
COUNT(*) as Count
FROM useforce
GROUP BY Incident_Type, Precinct_Sector, Precinct, Occured_date_time
ORDER BY Precinct_Sector DESC, Precinct, Occured_date_time DESC
INTO OUTFILE {} 
FIELDS ENCLOSED BY '"' 
TERMINATED BY ',' 
ESCAPED BY '"' 
LINES TERMINATED BY '\\r\\n');
'''.format(report_4)

queries = [query_1, query_2, query_3, query_4]

########################################################################################
