import sqlite3


# Function to initialize the database
def init_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS clips
                 (id INTEGER PRIMARY KEY,
                  url TEXT,
                  video_url TEXT,
                  broadcaster_id INTEGER,
                  broadcaster_name TEXT,
                  game_id INTEGER,
                  title TEXT,
                  view_count INTEGER,
                  created_at TEXT,
                  thumbnail_url TEXT,
                  duration INTEGER,
                  path TEXT
                  deleted INTEGER DEFAULT 0)"""
    )
    conn.commit()
    conn.close()


# Function to insert a Clip instance into the database
def insert_clip(db_name, clip):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute(
        """INSERT INTO clips 
        (id, 
        url,
        video_url, 
        broadcaster_id, 
        broadcaster_name, 
        game_id, 
        game_name,
        title, 
        view_count, 
        created_at, 
        thumbnail_url, 
        duration, 
        path) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            clip.id,
            clip.url,
            clip.broadcaster_id,
            clip.broadcaster_name,
            clip.game_id,
            clip.game_name,
            clip.title,
            clip.view_count,
            clip.created_at.isoformat(),
            clip.thumbnail_url,
            clip.duration,
            clip.path,
        ),
    )

    conn.commit()
    conn.close()
