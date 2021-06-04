# Import Python packages 
import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv
from sql_queries import *
from cassandra.cluster import Cluster

def show_session_history_select_result(rows):
    print("## Query 1:  Give me the artist, song title and song's length in the music app history that was heard during  sessionId = 338, and itemInSession = 4")
    for row in rows:
        print (row.artist, row.song, row.length)

def show_user_session_history_select_result(rows):
    print("## Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182")
    for row in rows:
        print (row.artist, row.song, row.firstname, row.lastname)

def show_song_history_select_result(rows):
    print("## Query 3: Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'")
    for row in rows:
        print (row.firstname, row.lastname)
        
def process_history(session, createTableQuery, insertQuery, selectQuery, func):
    """
    Description: This function can be used to read the file in the filepath (data/song_data)
    to get the song and artist info and used to populate the songss and artists dim tables.

    Arguments:
        cur: the cursor object. 
        filepath: song data file path. 

    Returns:
        None
    """
    
    
    try:
        session.execute(createTableQuery)
    except Exception as e:
        print(e)  

    # We have provided part of the code to set up the CSV file. Please complete the Apache Cassandra code below#
    file = 'event_datafile_new.csv'

    with open(file, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        for line in csvreader:
            ## Assign which column element should be assigned for each column in the INSERT statement.
            ## For e.g., to INSERT artist_name and user first_name, you would change the code below to `line[0], line[1]`
            session.execute(insertQuery, (line[0], line[1], line[2], int(line[3]), line[4], float(line[5]), line[6], line[7], int(line[8]), line[9], int(line[10])))
            
    
    ## Add in the SELECT statement to verify the data was entered into the table
    try:
        rows = session.execute(selectQuery)
    except Exception as e:
        print(e)
        
    func(rows)


def process_data(filepath):
    """
    Description: This function can be used to read the file in the specified filepath
    to get the json file and used to execute specified function.

    Arguments:
        cur: the cursor object. 
        filepath: song data file path. 

    Returns:
        None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.csv'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    
    # initiating an empty list of rows that will be generated from each file
    full_data_rows_list = [] 

    # for every filepath in the file path list 
    for f in all_files:
        # reading csv file 
        with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
            next(csvreader)

            # extracting each data row one by one and append it        
            for line in csvreader:
                #print(line)
                full_data_rows_list.append(line) 
        

    # uncomment the code below if you would like to get total number of rows 
    #print(len(full_data_rows_list))
    # uncomment the code below if you would like to check to see what the list of event data rows will look like
    #print(full_data_rows_list)

    # creating a smaller event data csv file called event_datafile_new csv that will be used to insert data into the \
    # Apache Cassandra tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
                    'level','location','sessionId','song','userId'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))

    # check the number of rows in your csv file
    with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
        print(sum(1 for line in f))
        
            
def main():
    """
    Description: This function is etl.py entrance
    to connect database and process csv data from data directory.

    Arguments:
        cur: the cursor object. 
        filepath: song data file path. 

    Returns:
        None
    """
    # This should make a connection to a Cassandra instance your local machine 
    # (127.0.0.1)

    
    cluster = Cluster()

    # To establish connection and begin executing queries, need a session
    session = cluster.connect()
    
    # Create a Keyspace 
    try:
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS udacity 
            WITH REPLICATION = 
            { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"""
        )
    except Exception as e:
        print(e)
        
    # Set KEYSPACE to the keyspace specified above
    try:
        session.set_keyspace('udacity')
    except Exception as e:
        print(e)
    
    process_data(filepath='event_data')
    
    ## Query 1:  Give me the artist, song title and song's length in the music app history that was heard during \
    ## sessionId = 338, and itemInSession = 4
    process_history(session, createTableQuery=session_history_table_create, insertQuery = session_history_insert, selectQuery=session_history_select, func=show_session_history_select_result)
    print("")
    
    ## Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name)\
    ## for userid = 10, sessionid = 182
    process_history(session, createTableQuery=user_session_history_table_create, insertQuery = user_session_history_insert, selectQuery=user_session_history_select, func=show_user_session_history_select_result)
    print("")
    
    ## Query 3: Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
    process_history(session, createTableQuery=song_history_table_create, insertQuery = song_history_insert, selectQuery=song_history_select, func=show_song_history_select_result)
    print("")
    
    ## drop tables
    for query in drop_table_queries:
        try:
            rows = session.execute(query)
        except Exception as e:
            print(e)
            
    session.shutdown()
    cluster.shutdown()

if __name__ == "__main__":
    main()