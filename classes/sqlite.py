import sqlite3


# Function to initialize the database
def init_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS clips
                 (id INTEGER PRIMARY KEY,
                  url TEXT,
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
        """INSERT INTO clips (id, url, broadcaster_id, broadcaster_name, game_id, title, view_count, created_at, thumbnail_url, duration, path) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            clip.id,
            clip.url,
            clip.broadcaster_id,
            clip.broadcaster_name,
            clip.game_id,
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


# Example usage
db_name = "clips.db"
init_db(db_name)

# Example Clip instance
clip = Clip(
    1,
    "http://example.com",
    123,
    "Broadcaster",
    456,
    "Game Title",
    1000,
    datetime.datetime.now(),
    "http://example.com/thumbnail.jpg",
    30,
    "/path/to/clip",
)

# Insert the clip into the database
insert_clip(db_name, clip)
