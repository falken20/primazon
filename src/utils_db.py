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
from rich.console import Console

# Load .env file
load_dotenv(find_dotenv())

# Create console object
console = Console()


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
        console.print(
            "Error getting connection to DB:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")
        return False


def drop_tables(cur):
    """
    Drop tables from database

    Args:
        cur (_cursor): Cursor from database
    """
    try:
        console.print("Drop table [bold]t_prices[/bold]...", style="blue")
        cur.execute('DROP TABLE IF EXISTS t_prices;')
        console.print(
            "Drop table [bold]t_products[/bold]...", style="blue")
        cur.execute('DROP TABLE IF EXISTS t_products;')
    except Exception as err:
        console.print(
            "Error dropping tables from DB:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


def create_table_products(cur):
    """
    Create t_products table

    Args:
        cur (_cursor): Cursor from database
    """
    try:
        console.print("Create table [bold]t_products[/bold]...", style="blue")
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
        console.print(
            "Error creating t_products:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


def create_table_prices(cur):
    """
    Create t_prices table

    Args:
        cur (_cursor): Cursor from database
    """
    try:
        console.print("Create table [bold]t_prices[/bold]...", style="blue")
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
        console.print(
            "Error creating t_prices:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


def grant_privileges(cur, user):
    """
    Grant privileges on tables for a role

    Args:
        cur (_type_): _description_
    """
    try:
        console.print(
            "Grant privileges on schema [bold]public[/bold]...", style="blue")
        cur.execute(f'GRANT ALL ON ALL TABLES IN SCHEMA public TO {user};')
        console.print(
            "Grant privileges in sequences on schema [bold]public[/bold]...", style="blue")
        cur.execute(
            f'GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {user};')
    except Exception as err:
        console.print(
            f"Error gratting privileges on tables for user {user}:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


def exec_sql_statement(sql):
    """
    Execute a sql statement

    Args:
        sql (str): Sql statement to execute

    Returns:
        list[Tuple]: Rows from execute sql statement
    """
    try:
        console.print(f"Executing sql statement: {sql}", style="blue")
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
        console.print(
            "Error executing sql statement:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


def main():
    """
    Main process to create the needed tables for the application
    """
    console.print("[bold green]Process starting...[/bold green]")

    try:
        console.print("Connecting with [bold]DB[/bold]...", style="blue")
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

        console.print("Closing connection [bold]DB[/bold]...", style="blue")
        cur.close()
        conn.close()
        console.print("[bold green]Process finished succesfully[/bold green]")

    except Exception as err:
        console.print(
            "Execution Error:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


if __name__ == "__main__":
    main()
