import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
from rich import print

# Load .env file
load_dotenv(find_dotenv())

print("Connecting with [bold]DB[/bold]...", style="blue")
conn = psycopg2.connect(
    host="localhost",
    database=os.environ['DB_DATABASE'],
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Create user and grant privileges
# cur.execute('CREATE USER %s WITH PASSWORD %s;', (user, password))
# cur.execute('GRANT ALL PRIVILEGES ON DATABASE %s TO %s;', (database, user))

# Execute a command: this creates a new table
print("Create table [bold]t_products[/bold] if not exist...", style="blue")
cur.execute('DROP TABLE IF EXISTS t_products;')
cur.execute('CREATE TABLE t_products '
            '(product_id serial PRIMARY KEY,'
            'product_url varchar (500) NOT NULL,'
            'product_desc varchar (150) NOT NULL,'
            'product_price float NOT NULL,'
            'product_date_added date DEFAULT CURRENT_TIMESTAMP,'
            'product_date_updated date);'
            )

print("Create table [bold]t_prices[/bold] if not exist...", style="blue")
cur.execute('DROP TABLE IF EXISTS t_prices;')
cur.execute('CREATE TABLE t_prices '
            '(price_id serial PRIMARY KEY,'
            'product_id varchar (500) NOT NULL,'
            'product_price float NOT NULL,'
            'product_date_added date DEFAULT CURRENT_TIMESTAMP,'
            'CONSTRAINT fk_products'
            '   FOREIGN KEY(product_id)'
	        '   REFERENCES t_products(product_id))'
            )

conn.commit()

print("Closing connection with [bold]DB[/bold]...", style="blue")
cur.close()
conn.close()
print("Process finished [bold]succesfully[/bold]", style="blue")

