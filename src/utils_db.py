# by Richi Rod AKA @richionline / falken20

# Functions for use the database without a ORM library

# Create user and grant privileges, it should be done before in the terminal, important the ';' at the end
# CREATE ROLE user LOGIN PASSWORD password;
# GRANT ALL PRIVILEGES ON DATABASE db TO user;
# GRANT CONNECT ON DATABASE my_db TO my_user;

import os
import sys
import psycopg2
from dotenv import load_dotenv, find_dotenv

from src.logger import Log, console

# Load .env file
load_dotenv(find_dotenv())


def get_db_connection():
    """
    Return a connection to the database

    Returns:
        connection: The connection to the database
    """
    try:
        return psycopg2.connect(
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            database=os.environ['DB_DATABASE'],
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
    except Exception as err:
        Log.error("Error getting connection to DB:", err, sys)
        return False


def drop_tables(cur):
    """
    Drop tables from database

    Args:
        cur (_cursor): Cursor from database
    """
    try:
        Log.info("Drop table [bold]t_prices[/bold]...")
        cur.execute('DROP TABLE IF EXISTS t_prices;')
        Log.info("Drop table [bold]t_products[/bold]...")
        cur.execute('DROP TABLE IF EXISTS t_products;')
    except Exception as err:
        Log.error("Error dropping tables from DB:", err, sys)


def create_table_products(cur):
    """
    Create t_products table

    Args:
        cur (_cursor): Cursor from database
    """
    try:
        Log.info("Create table [bold]t_products[/bold]...")
        cur.execute('CREATE TABLE t_products '
                    '(product_id serial PRIMARY KEY,'
                    'product_url varchar (500) NOT NULL,'
                    'product_desc varchar (150) NOT NULL,'
                    'product_url_photo varchar (500) NOT NULL,'
                    'product_price float,'
                    'product_rating varchar(50),'
                    'product_reviews varchar(100),'
                    'product_min_price float,'
                    'product_max_price float,'
                    'product_date_added date DEFAULT CURRENT_TIMESTAMP,'
                    'product_date_updated date);'
                    )
    except Exception as err:
        Log.error("Error creating t_products:", err, sys)


def create_table_prices(cur):
    """
    Create t_prices table

    Args:
        cur (_cursor): Cursor from database
    """
    try:
        Log.info("Create table [bold]t_prices[/bold]...")
        cur.execute('CREATE TABLE t_prices '
                    '(price_id serial PRIMARY KEY,'
                    'product_id serial,'
                    'product_price float NOT NULL,'
                    'price_date_added date DEFAULT CURRENT_TIMESTAMP,'
                    'CONSTRAINT fk_products'
                    '   FOREIGN KEY(product_id)'
                    '   REFERENCES t_products(product_id))'
                    )
    except Exception as err:
        Log.error("Error creating t_prices:", err, sys)


def grant_privileges(cur, user):
    """
    Grant privileges on tables for a role

    Args:
        cur (_type_): _description_
    """
    try:
        Log.info("Grant privileges on schema [bold]public[/bold]...")
        cur.execute(f'GRANT ALL ON ALL TABLES IN SCHEMA public TO {user};')
        Log.info(
            "Grant privileges in sequences on schema [bold]public[/bold]...")
        cur.execute(
            f'GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {user};')
    except Exception as err:
        Log.error(
            f"Error gratting privileges on tables for user {user}:", err, sys)


def exec_sql_statement(sql):
    """
    Execute a sql statement

    Args:
        sql (str): Sql statement to execute

    Returns:
        list[Tuple]: Rows from execute sql statement
    """
    try:
        Log.info(f"Executing sql statement: {sql}")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        # For INSERT, DELETE, etc statement fetchall() return Exception, avoid this with cursor.description()
        result = cur.fetchall() if cur.description else []
        cur.close()
        conn.close()

        return result
    except Exception as err:
        Log.error("Error executing sql statement:", err, sys)


def main():
    """
    Main process to create the needed tables for the application
    """
    Log.info("Process starting...")

    try:
        Log.info("Connecting with [bold]DB[/bold]...")
        conn = get_db_connection()

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Ask if we want to drp the tables if they exist
        if input("Could you drop the tables if they exist (y/n)? ") in ["Y", "y"]:
            drop_tables(cur)

        # Creates needed tables
        create_table_products(cur)
        create_table_prices(cur)

        # Grant privileges on tables and on sequences. IT SHOULD BE USED MASTER USER
        grant_privileges(cur, os.environ['DB_USERNAME'])

        conn.commit()

        Log.info("Closing connection [bold]DB[/bold]...")
        cur.close()
        conn.close()
        Log.info("Process finished succesfully")

    except Exception as err:
        Log.error("Execution Error:", err, sys)


if __name__ == "__main__":
    console.rule("Primazon DB Utils")
    main()
