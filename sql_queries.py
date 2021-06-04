# DROP TABLES

session_history_table_drop = "drop table if exists session_history_table"
user_session_history_table_drop = "drop table if exists user_session_history"
song_history_table_drop = "drop table if exists song_history"

# CREATE TABLES 
# the sequence of columns match that of the sequence of PRIMARY KEYs.

session_history_table_create = (""" 
CREATE TABLE IF NOT EXISTS session_history
    (
        sessionId decimal, itemInSession decimal, 
        artist text, firstName text, gender text, lastName text,length decimal, 
        level text, location text, song text, userId decimal, 
        PRIMARY KEY (sessionId, itemInSession)
    )
""")

## Set userId and sessionId as a COMPOSITE PARTITIOIN KEY.
## That way, itemInSession will become the only CLUSTERING COLUMN and the data will be ordered as required.
user_session_history_table_create = (""" 
CREATE TABLE IF NOT EXISTS user_session_history
    (
        userId decimal, sessionId decimal, itemInSession decimal, 
        artist text, firstName text, gender text, lastName text, length decimal, level text, location text, song text, 
        PRIMARY KEY ((userId, sessionId), itemInSession)
    )
""")

## should consider the scenario where two or more person with the same first and last name are listening to the same song.
song_history_table_create = ("""
CREATE TABLE IF NOT EXISTS song_history
    (
        song text, userId decimal, 
        artist text, firstName text, gender text, itemInSession decimal, lastName text, 
        length decimal, level text, location text, sessionId decimal,  
        PRIMARY KEY (song, userId)
    )
""")

# INSERT
session_history_insert = ("""
insert into session_history 
    (artist, firstName, gender, itemInSession, lastName, length, level, location, sessionId, song, userId)
    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""")

user_session_history_insert = ("""
insert into user_session_history 
    (artist, firstName, gender, itemInSession, lastName, length, level, location, sessionId, song, userId)
    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""")

song_history_insert = ("""
insert into song_history
    (artist, firstName, gender, itemInSession, lastName, length, level, location, sessionId, song, userId)
    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""")

# FIND SONGS

session_history_select = ("""
select artist, song, length from session_history where sessionId = 338 and itemInSession = 4
""")

user_session_history_select = ("""
select artist, song, firstName, lastName from user_session_history where userId = 10 and sessionId = 182
""")

song_history_select = ("""
select firstName, lastName from song_history where song='All Hands Against His Own'
""")


# QUERY LISTS

create_table_queries = [session_history_table_create, user_session_history_table_create, song_history_table_create]
drop_table_queries = [session_history_table_drop, user_session_history_table_drop, song_history_table_drop]