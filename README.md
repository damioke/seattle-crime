# seattle_crime

## Requirements
- A WampServer with a MySQL database 'mysql5.6.17' was used for this project
- Install a WampServer Server
- Create a data warehouse in MySQL database with name: seattle_crime
- Make changes to the necessary credentials in the variable.py file
- Download the data files and move them into the following location:
- u_of_f_data.csv into => C:\wamp\bin\mysql\mysql5.6.17\data\seattle_crime\u_of_f_data.csv
- crime_data.csv into => C:\wamp\bin\mysql\mysql5.6.17\data\seattle_crime\crime_data.csv
- Move all the scripts to into this location: C:\wamp\bin\mysql\mysql5.6.17\bin
- From your command prompt navigate to this location where you have all your scripts: C:\wamp\bin\mysql\mysql5.6.17\bin\
- Viola, execute your program by running this script only: ./job.sh


## TO RUN THE YACHT PROGRAM
- Make sure the tables you are using for test cases are dropped in MySQL db: seattle_crime
- Make sure the reports you are using for test cases are dropped in: C:\wamp\bin\mysql\mysql5.6.17\data\seattle_crime
- Navigate to where all the scripts and program are present there: C:\wamp\bin\mysql\mysql5.6.17\bin
- Right click to click gitbash cmd line. 
- Run: ./job.sh