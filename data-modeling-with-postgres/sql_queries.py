# Drop tables queries
drop_songplay = "DROP TABLE IF EXISTS songplay"
drop_users = "DROP TABLE IF EXISTS users"
drop_songs = "DROP TABLE IF EXISTS songs"
drop_artists = "DROP TABLE IF EXISTS artists"
drop_time = "DROP TABLE IF EXISTS time"

# Create tables queries

create_songplay = """CREATE TABLE IF NOT EXISTS songplay(
                    songplay_id SERIAL PRIMARY KEY,
                    start_time date REFERENCES time(start_time), 
                    user_id int NOT NULL REFERENCES users(user_id), 
                    level text, 
                    song_id text REFERENCES songs(song_id), 
                    artist_id text REFERENCES artists(artist_id), 
                    session_id int, 
                    location text, 
                    user_agent text
                    )
                    """

create_users = """CREATE TABLE IF NOT EXISTS users(
                user_id int PRIMARY KEY, 
                first_name varchar NOT NULL, 
                last_name varchar NOT NULL, 
                gender varchar(1),
                level varchar
                )"""

create_songs = """CREATE TABLE IF NOT EXISTS songs(
                song_id varchar PRIMARY KEY, 
                title text NOT NULL,
                artist_id varchar, 
                year int, 
                duration numeric
                )"""

create_artists = """CREATE TABLE IF NOT EXISTS artists(
                artist_id text PRIMARY KEY,
                name text NOT NULL, 
                location text,
                latitude float, 
                longitude float
                )"""

create_time = """CREATE TABLE IF NOT EXISTS time(
                start_time date PRIMARY KEY,
                hour int, 
                day int, 
                week int, 
                month int, 
                year int, 
                weekday text
                )"""

songplay_insert = ("""
    INSERT INTO songplay
    (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")

users_insert = ("""
   INSERT INTO users
    (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
""")

artists_insert = ("""
    INSERT INTO artists
    (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING;
""")

songs_insert = ("""
    INSERT INTO songs
    (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING;
""")

time_insert = ("""
    INSERT INTO time
    (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS
#     AND songs.duration = %s
song_select = ("""
    SELECT songs.song_id, artists.artist_id FROM songs 
    JOIN artists ON songs.artist_id = artists.artist_id
    WHERE songs.title = %s AND artists.name = %s AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [create_users, create_artists, create_songs, create_time, create_songplay]
drop_table_queries = [drop_users, drop_artists, drop_songs, drop_time, drop_songplay]
