# Creates a database
import psycopg2, sys


# Connect to (default) postgres database
try:
    connection = psycopg2.connect("host=localhost dbname=postgres user=postgres password=password")
    print("Connected to database: postgres")
except psycopg2.Error as e:
    print("The following error occurred: \n", e)
    sys.exit(1)

# Set autocommit to True
connection.set_session(autocommit=True)


# Establish cursor
try:
    cursor = connection.cursor()
    print("Got cursor successfully")
except Exception as e:
    print("Error occurred while getting cursor to database: postgres\n", e)
    sys.exit(1)

# Create news_analytics database for our application
try:
    cursor.execute("CREATE DATABASE news_analytics")
    print("Created database: news_analytics")
except Exception as e:
    print(e)

# Close connection with postgres database
connection.close()
print("Closed connection with database: postgres")

# Connect to news_analytics database
try:
    connection = psycopg2.connect("host=localhost dbname=news_analytics user=postgres password=password")
    print("Connected to database: news_analytics")
except psycopg2.Error as e:
    print("The following error occurred: \n", e)
    sys.exit(1)

# Establish cursor
try:
    cursor = connection.cursor()
    print("Got cursor successfully")
except Exception as e:
    print("Error occurred while getting cursor to database: news_analytics \n", e)
# Create table articles
cursor.execute("CREATE TABLE IF NOT EXISTS articles(\
               article_url VARCHAR(200) PRIMARY KEY,\
               headline VARCHAR(250) NOT NULL,\
               thesis_length_words INT,\
               thesis_length_chars INT,\
               publication_datetime TIMESTAMP NOT NULL,\
               article_category VARCHAR(50) NOT NULL,\
               number_of_views INT NOT NULL,\
               article_source VARCHAR(50) NOT NULL)")

# Close connection with news_analytics database
connection.close()
print("Closed connection with database: news_analytics")