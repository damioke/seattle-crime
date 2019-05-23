import os
import sys
import pymysql
from variables import (datawarehouse_name, useforce_tbl, crime_tbl, host, user, password, report_1,
report_2, report_3, report_4, useforce_file, crimes_file)
from sql_queries import (create_dw_query, load_queries, queries)

def main():
    
    print('Starting etl')
    
    try:
        # connect to MySQL server
        con = pymysql.connect(
            host=host,
            user=user,
            password=password,
            autocommit=True,
            local_infile=1,
            charset='utf8mb4')
        print('Connection established to MySQL database server: {}'.format(host))
        
        # create a cursor object
        cur = con.cursor()
        print('Connection cursor object created')
        
        # select a data warehouse
        #cur.execute('USE seattle_crime')
        cur.execute('USE {}'.format(datawarehouse_name))
        print('Selected {} data warehouse for loading'.format(datawarehouse_name))
        
        #iterate over sql queries to execute
        for q in create_dw_query:
            cur.execute(q)
        print('All tables were created successfully')
    
        #iterate over sql queries to execute
        for q in load_queries:
            cur.execute(q)        

        # export to csv
        for q in queries:
            cur.execute(q)
            rows = cur.fetchall()
        print('All files were successfully exported')
        
    except Exception as e:
        print('Error: {}'.format(str(e)))
        sys.exit(1)
        
    #Close connection
    finally:
        con.close()
        
if __name__ == "__main__":
    main()