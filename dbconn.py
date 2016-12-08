import sqlite3

conn = sqlite3.connect('suggestbox.db')
mycursor = conn.cursor()

def create_table():
    mycursor.execute ('CREATE TABLE IF NOT EXISTS users(user_id BIGINT, user_name TEXT, user_username VARCHAR, user_password VARCHAR) ')

def data_entry():
    mycursor.execute ("INSERT INTO users VALUES (1, 'batian', 'bmuthoga', '1234')")
    conn.commit()
    mycursor.close()
    conn.close()

create_table()

data_entry()
