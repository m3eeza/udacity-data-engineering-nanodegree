# Project data modeling with PostgreeSQL

This project is the first project of  Udacity's Data Engineering nano-degree.

### Introduction
A startup called Sparkify wants to analyze the data they've been collecting songs and user activity on their new 
music streaming app. The analytics team is particularly interested in understanding what songs users are listening 
to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user 
activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play 
analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. 
You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from 
Sparkify and compare your results with their expected results.

### Project Description
In this project, you'll apply what you've learned on data modeling with Postgres and build an ETL pipeline using 
Python. To complete the project, you will need to define fact and dimension tables for a star schema for a 
particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories i
nto these tables in Postgres using Python and SQL.

### Data Model
The data model we choose to implement is a star model. It is the typical schema for a Data Warehouse. The tables being:

#### Fact Table

**Table songplay**

| COLUMN  	| TYPE  	| CONSTRAINT  	|
|---	|---	|---	|	
|   songplay_id	| SERIAL  	|   PRIMARY KEY	| 
|   start_time	|   bigint	|   NOT NULL	| 
|   user_id	|   int	|   NOT NULL	| 
|   level	|   varchar |   	| 
|   song_id	|   varchar	|   	| 
|   artist_id	|   varchar	|   	| 
|   session_id	|   int	|   	| 
|   location	|   text	|   	| 
|   user_agent	|   text	|   	| 

The songplay_id field is the primary key and it is an auto-incremental value.

The query to insert data on this table is:

``INSERT INTO songplay (start_time, user_id, level,song_id, artist_id, session_id, location, user_agent) \
 VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)``
 
 #### Dimensions Tables
 I've created one table for each dimension of the **Fact Table**
 
 **Table users**
 
 | COLUMN  	| TYPE  	| CONSTRAINT  	|
|---	|---	|---	|	
|   user_id	| int  	|   PRIMARY KEY	| 
|   first_name	|   varchar	|  	| 
|   last_name	|   varchar	|  	| 
|   gender	|   varchar(1) |   	| 
|   level	|   varchar	|   	| 

 
 The query to insert data on this table is:
 
 ``INSERT INTO users (user_id, first_name, last_name, gender, level) 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (user_id) 
        DO UPDATE
        SET first_name = EXCLUDED.first_name, last_name = EXCLUDED.last_name,
        gender = EXCLUDED.gender, level = EXCLUDED.level``

An alternative is change the target of *ON CONFLICT*. I assumed the info about users don't change. But it 
could be probably better to DO UPDATE action in order to get the latest info about a user.

**Table songs**

 | COLUMN  	| TYPE  	| CONSTRAINT   	|
|---	|---	|---	|	
|   song_id	| varchar  	|   PRIMARY KEY	| 
|   title	|   text	|  	| 
|   artist_id	|   varchar	|   	| 
|   year	|   int |   	| 
|   duration	|   numeric	|   	| 

 The query to insert data on this table is:
 
``INSERT INTO songs (song_id, title, artist_id, year, duration) 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (song_id) 
        DO UPDATE
        SET title = EXCLUDED.title, artist_id = EXCLUDED.artist_id,
        year = EXCLUDED.year, duration = EXCLUDED.duration ``

**Table artists**

 | COLUMN  	| TYPE  	| CONSTRAINT   	|
|---	|---	|---	|	
|   artist_id	| varchar  	|   PRIMARY KEY	| 
|   name	|   varchar	|   	| 
|   location	|   text	|   	| 
|   latitude	|   decimal	|   	| 
|   longitude	|   decimal |   	| 


 The query to insert data on this table is:
 
``INSERT INTO artists (artist_id, name, location, latitude, longitude) 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (artist_id) 
        DO UPDATE
        SET name = EXCLUDED.name, location = EXCLUDED.location,
        latitude = EXCLUDED.latitude, longitude = EXCLUDED.longitude``

**Table time**
 
 | COLUMN  	| TYPE  	| CONSTRAINT   	|
|---	|---	|---	|	
|   start_time	| bigint  	|   PRIMARY KEY	| 
|   hour	|   int	|   	| 
|   day	|   int	|   	| 
|   week	|   int	|   	| 
|   month	|   int	|   	| 
|   year	|   int	|   	| 
|   weekday	|   varchar	|   	| 

 The query to insert data on this table is:
 
``INSERT INTO time (start_time, hour, day, week, month, year, weekday) 
VALUES (%s, %s, %s, %s, %s, %s, %s) 
ON CONFLICT (start_time) 
DO NOTHING``

### Files in Python
#### ETL Pipeline

The ETL script is in the file **etl.py** and is divided in the next sections:

1. Connect to the database.
2. Process **song files**.
    1. Insert song data into **songs** table. 
    2. Insert artist data into **artists** table. 
3. Process **log_files**.
    1. Insert ts (unix timestamp) in **time** table.
        1. from the field **ts** we extract year, day, hour, week, month and day of the week.
    2. Insert user info in **users** table.
    3. Insert songplay records into **songplay** table. In this case we need an additional select to get the 
    artist_id and the artist_id. This is very important for the star schema. 
4. Disconnect and finish.
    
#### sql_queries.py

This file contains all the queries to the database. 
 
 In this file are:
 1. All CREATE statements for all the tables.
 2. All INSERT statements for all the tables.
 3. The select to get artist_id and song_id in order to fill the songplay table.


### Local Execution

For local execution you can use Postgres SQL docker:

- Download docker image:

`` docker pull postgres ``

- Execute docker:

``docker run --name postgres --rm  -p 5432:5432 -e -d postgres``

- Connect string:

``"host=127.0.0.1 dbname=postgres user=postgres password=postgres port=5432" ``


