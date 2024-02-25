from sqlalchemy import create_engine
import pandas as pd

data = {
    'Name': ['John', 'Anna', 'Peter', 'Linda'],
    'Age': [28, 35, 40, 25],
    'City': ['New York', 'Paris', 'London', 'Sydney']
}

# Create the DataFrame
df = pd.DataFrame(data)

def df_to_sql(dataframe, table):
    # PostgreSQL connection parameters
    username = 'postgres'
    password = 'password'
    host = 'localhost'
    port = '5432'
    database_name = 'news_analytics'

    # Construct the connection string
    connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'

    # Connect to db
    db_engine = create_engine(connection_string)
    dataframe.to_sql(table, db_engine, if_exists="append", index=False)
    sql = "SELECT * FROM articles;"
    new_df = pd.read_sql(sql, con=db_engine)
    print(new_df)
    db_engine.dispose()



