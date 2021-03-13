import sqlite3


class Controller:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
           userid INTEGER NOT NULL UNIQUE,
           first_name TEXT NULL,
           last_name TEXT NULL,
           username TEXT NULL,
           language_code TEXT NULL);
        """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS messages(
           message_id INTEGER NULL,
           userid INTEGER NOT NULL,
           date TEXT NULL,
           text TEXT NULL);
        """)
        self.conn.commit()

    def write_user(self, userid, first_name, last_name, username, language_code):
        if userid:
            user = (userid, first_name, last_name, username, language_code)
            self.cur.execute("""INSERT INTO users (userid, first_name, last_name, username, language_code) 
                                            VALUES(?, ?, ?, ?, ?);""", user)
            self.conn.commit()
        else:
            return "No user id"

    def write_message(self, message_id, userid, date, text):
        if message_id:
            message = (message_id, userid, date, text)
            self.cur.execute("""INSERT INTO messages (message_id, userid, date, text) 
                                                       VALUES(?, ?, ?, ?);""", message)
            self.conn.commit()
        else:
            return "No message id"
    def __del__(self):
        self.cur.close()
        self.conn.close()
