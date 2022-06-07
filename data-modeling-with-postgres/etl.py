import os
import psycopg2
import pandas as pd
from sql_queries import *


def process_data(cur, conn, file_path, process_func):
    """Walks through all files nested under filepath, and processes all logs found.
    Parameters:
        cur (psycopg2.cursor()): Cursor of the sparkifydb database
        conn (psycopg2.connect()): Connection to the sparkifydb database
        file_path (str): Filepath parent of the logs to be analyzed
        process_func (python function): Function to be used to process each log
    Returns:
        paths of processed files
    """
    file_paths = []
    for root, _, files in os.walk(file_path):
        file_paths.extend([os.path.join(root, file) for file in files if file.endswith(".json")])

    # get total number of files found
    num_files = len(file_paths)
    print(f'{num_files} files found in {file_path}')

    for i, file in enumerate(file_paths):
        process_func(cur, file)
        conn.commit()
        print(f'{i + 1}/{num_files} files processed.')

    return file_paths


def process_song_file(cur, file_path):
    """Reads a song file, selects needed fields and inserts them into song and artist tables.
    Parameters:
        cur (psycopg2.cursor()): Cursor of the sparkifydb database
        file_path (str): Filepath of the file to be analyzed
    """
    # open song file
    df = pd.read_json(file_path, lines=True)
    for value in df.values:
        (_, artist_id, artist_latitude, artist_longitude, artist_location,
         artist_name, song_id, title, duration, year) = value
        # insert artist record
        artist_data = [artist_id, artist_name, artist_location, artist_longitude, artist_latitude]
        cur.execute(artists_insert, artist_data)
        # insert song record
        song_data = [song_id, title, artist_id, year, duration]
        cur.execute(songs_insert, song_data)


def process_log_file(cur, file_path):
    """Reads user activity log file row by row, filters by NextSong, selects needed fields, transforms them and inserts
    them into time, user and songplay tables.
            Parameters:
                cur (psycopg2.cursor()): Cursor of the sparkifydb database
                file_path (str): Filepath of the file to be analyzed
    """
    # open log file
    df = pd.read_json(file_path, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime format
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = [[line, line.hour, line.day, line.week, line.month, line.year, line.day_name()] for line in t]
    for row in time_data:
        cur.execute(time_insert, row)

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for _, row in user_df.iterrows():
        cur.execute(users_insert, row)

    # insert songplay records
    for _, row in df.iterrows():
        # get song_id and artist_id from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        print(results) if results else None
        song_id, artist_id = results if results else (None, None)

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), int(
            row.userId), row.level, song_id, artist_id, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_insert, songplay_data)


def etl():
    """Function used to extract, transform all data from song and user activity logs and load it into a Postgres DB
        Usage: python etl.py
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, file_path='data/song_data', process_func=process_song_file)
    process_data(cur, conn, file_path='data/log_data', process_func=process_log_file)

    conn.close()


if __name__ == "__main__":
    etl()
