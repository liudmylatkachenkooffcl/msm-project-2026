import sqlite3

conn = sqlite3.connect("msm.db")
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

def edit_post(post_id, text, author_id, image):
    cur.execute("UPDATE Post SET text = ?, image = ?", (text, image))
    conn.commit()

def edit_user(username, email, first_name, last_name):
    cur.execute("UPDATE Post SET username = ?, email = ?, first_name = ?, last_name = ?",
                (username, email, first_name, last_name))
    
def recall_post(post_id):
    cur.execute("SELECT Post.post_id, Post.text, Post.image," \
    "Post.author_id, User.user_id, User.username, User.first_name, " \
    "User.last_name, User.profile_pic FROM Post " \
    "INNER JOIN User ON Post.author_id = User.user_id WHERE Post.post_id = ?", (post_id,))
    to_front = cur.fetchone()
    return to_front

def recall_post_chronologic(user_id):
    cur.execute("SELECT Post.post_id, Post.text, Post.image," \
    "Post.author_id, User.user_id, User.username, User.first_name, " \
    "User.last_name, User.profile_pic FROM Post " \
    "INNER JOIN User ON Post.author_id = User.user_id WHERE User.user_id = ?" \
    "ORDER BY Post.created DESC", (user_id,))
    to_front = cur.fetchall()
    return(to_front)

def recall_feed(seen_post_id, limit=10):
    if not seen_post_id:
        cur.execute("SELECT Post.post_id, Post.text, Post.image," \
        "Post.author_id, User.user_id, User.username, User.first_name, " \
        "User.last_name, User.profile_pic FROM Post " \
        "INNER JOIN User ON Post.author_id = User.user_id " \
        "ORDERED BY RANDOM() LIMIT 20")
        to_front = cur.fetchall()
        return to_front
    
    else:
        placeholders = ", ".join("?" for i in limit )
        cur.execute(f"SELECT Post.post_id, Post.text, Post.image," \
        "Post.author_id, User.user_id, User.username, User.first_name, " \
        "User.last_name, User.profile_pic FROM Post " \
        "INNER JOIN User ON Post.author_id = User.user_id " \
        "WHERE Post.post_id NOT IN ({placeholders})" \
        "ORDERED BY RANDOM() LIMIT ?", seen_post_id + [limit])
        to_front = cur.fetchall()
        return to_front
    


'''tipy na przyszłość: 1.) Pamiętaj o porządku statements: Select->Do smth.(np.join)->Sort and filter
2.) Pamiętaj pakować zmienne do podstawienia w tuple(nawet pojedyńcze)
3.) Wybieraj kiedy masz x = cur.fetchone albo fetchall(lista z tuplami)
4.) Inner join - rekordy tylko z parami w tabeli 2
    Left join - wyświetla wszystko z lewej tabeli, nawet jeżeli nie ma dopasowań z 2. Podobnie z Right Join 
5.) Pisz wszystkie polecenia razem'''
