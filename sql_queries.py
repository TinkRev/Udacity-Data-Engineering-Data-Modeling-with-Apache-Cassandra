# DROP TABLES

session_history_table_drop = "drop table if exists session_history_table"
user_session_history_table_drop = "drop table if exists user_session_history"
song_history_table_drop = "drop table if exists song_history"

# CREATE TABLES

session_history_table_create = (""" 
CREATE TABLE IF NOT EXISTS session_history
    (
        artist text, 
        firstName text, 
        gender text, 
        itemInSession decimal, 
        lastName text, 
        length decimal, 
        level text, 
        location text, 
        sessionId decimal, 
        song text, 
        userId decimal, 
        PRIMARY KEY (sessionId, itemInSession)
    )
""")

user_session_history_table_create = (""" 
CREATE TABLE IF NOT EXISTS user_session_history
    (
        artist text, 
        firstName text, 
        gender text, 
        itemInSession decimal, 
        lastName text, 
        length decimal, 
        level text, 
        location text, 
        sessionId decimal, 
        song text, 
        userId decimal, 
        PRIMARY KEY (userId, sessionId, itemInSession)
    )
""")

song_history_table_create = ("""
CREATE TABLE IF NOT EXISTS song_history
    (
        artist text, 
        firstName text, 
        gender text, 
        itemInSession decimal, 
        lastName text, 
        length decimal, 
        level text, 
        location text, 
        sessionId decimal, 
        song text, 
        userId decimal, 
        PRIMARY KEY (song, firstName, lastName)
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