import pandas as pd

# Load the cleaned Food Delivery dataset
df = pd.read_csv("food_delivery_cleaned.csv")

# Check the dataset
print("Dataset loaded successfully!")
print("Total rows:", df.shape[0])
print("Total columns:", df.shape[1])

# Display first 5 rows
print(df.head())

# Check column names
print(df.columns.tolist())

from sqlalchemy import create_engine, URL, text

# MySQL connection details
username = "root"
password = "Enter Password"
host = "localhost"
port = 3306

# Connect to MySQL Server
server_url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host=host,
    port=port
)

server_engine = create_engine(server_url)

# Create database
with server_engine.connect() as connection:
    connection.execute(
        text("CREATE DATABASE IF NOT EXISTS food_delivery_db")
    )
    connection.commit()

print("Database created successfully!")

# Connect to the project database
db_url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host=host,
    port=port,
    database="food_delivery_db"
)

engine = create_engine(db_url)

# Test connection
with engine.connect() as connection:
    result = connection.execute(text("SELECT DATABASE()"))
    print("Connected to:", result.scalar())

server_engine.dispose()
engine.dispose()


df.to_sql(
    name="food_orders",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000
)

print("Data inserted into MySQL successfully!")