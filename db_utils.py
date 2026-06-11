import sqlite3

conn = sqlite3.connect(msm.db)
cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON;") #to not accidentally create post from non-existing user.
cur.execute('''
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY UNIQUE DEFAULT (abs(random())), 
        username TEXT NOT NULL UNIQUE CHECK (length(username) >= 4 AND length(username) <= 30), 
        email TEXT NOT NULL UNIQUE, 
        password TEXT NOT NULL CHECK (length(password) >= 8 AND length(password) <= 20), 
        first_name TEXT NOT NULL CHECK (length(first_name) >= 4 AND length(first_name) <= 30), 
        last_name TEXT CHECK (length(last_name) <= 30), 
        profile_pic BLOB, 
        bio TEXT CHECK (length(bio) <= 400), 
        is_active BOOLEAN DEFAULT 1, 
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''') #all columns have their own line in this command

cur.execute('''CREATE TABLE IF NOT EXISTS Post (
        post_id TEXT PRIMARY KEY UNIQUE DEFAULT (lower(hex(randomblob(16)))), 
        text TEXT NOT NULL, 
        image BLOB, 
        author_id INTEGER NOT NULL, 
        created DATETIME DEFAULT CURRENT_TIMESTAMP, 
        FOREIGN KEY (author_id) REFERENCES User (user_id) 
        )
''')

def register_user(username, email, password, first_name, last_name):
    cur.execute("INSERT INTO USER (username, email, password, first_name, last_name) "
                "VALUES (?, ?, ?, ?, ?)", (username, email, password, first_name, last_name))
    conn.commit()

def create_post(post_id, text, author_id, image):
    cur.execute("INSERT INTO Post (post_id, text, author_id, image) "
                "VALUES (?, ? , ? , ?)", (post_id, text, author_id, image))
    conn.commit()

# def edit_post
