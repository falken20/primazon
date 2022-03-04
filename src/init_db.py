# by Richi Rod AKA @richionline / falken20

# Create user and grant privileges, it should be done before in the terminal, important the ';' at the end
# CREATE ROLE user LOGIN PASSWORD password;
# GRANT ALL PRIVILEGES ON DATABASE db TO user;
# GRANT CONNECT ON DATABASE my_db TO my_user;

import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
from rich.console import Console

# Load .env file
load_dotenv(find_dotenv())


def main():
    console = Console()
    console.print("[bold green]Process starting...[/bold green]")

    try:
        console.print("Connecting with [bold]DB[/bold]...", style="blue")
        conn = psycopg2.connect(
            host="localhost",
            database=os.environ['DB_DATABASE'],
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Ask if we want to drp the tables if they exist
        if input("Could you drop the tables if they exist (y/n)? ") in ["Y", "y"]:
            console.print("Drop table [bold]t_prices[/bold]...", style="blue")
            cur.execute('DROP TABLE IF EXISTS t_prices;')
            console.print("Drop table [bold]t_products[/bold]...", style="blue")
            cur.execute('DROP TABLE IF EXISTS t_products;')

        # Execute a command: this creates a new table
        console.print("Create table [bold]t_products[/bold]...", style="blue")
        cur.execute('CREATE TABLE t_products '
                    '(product_id serial PRIMARY KEY,'
                    'product_url varchar (500) NOT NULL,'
                    'product_desc varchar (150) NOT NULL,'
                    'product_price float NOT NULL,'
                    'product_date_added date DEFAULT CURRENT_TIMESTAMP,'
                    'product_date_updated date);'
                    )

        console.print("Create table [bold]t_prices[/bold]...", style="blue")
        cur.execute('CREATE TABLE t_prices '
                    '(price_id serial PRIMARY KEY,'
                    'product_id serial,'
                    'product_price float NOT NULL,'
                    'product_date_added date DEFAULT CURRENT_TIMESTAMP,'
                    'CONSTRAINT fk_products'
                    '   FOREIGN KEY(product_id)'
                    '   REFERENCES t_products(product_id))'
                    )

        conn.commit()

        console.print(
            "Closing connection with [bold]DB[/bold]...", style="blue")
        cur.close()
        conn.close()
        console.print("[bold green]Process finished succesfully[/bold green]")

    except Exception as err:
        console.print(f"[red bold]EXECUTION ERROR: {format(err)}")
        return False


if __name__ == "__main__":
    main()
