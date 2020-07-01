import psycopg2
from pathlib import Path
from sql-queries import create_table_queries, insert_table_queries

path_to_project = "/home/ubuntu/Fake-Book" #replace with your own path
project_folder = Path(path_to_project)

database_name = 'postgres' #replace these with your own name/user/host
user = 'postgres'
host = 'localhost'
_key_file = project_folder / "key-file.txt"

# Make sure there is a file called "key-file.txt" in your Fake-Book file,
# whose first line is the password to your database.

with _key_file.open() as key_file:
    input_list = key_file.readlines()

password = input_list[0]



def create_database():

    # connect to default database
    login_info = "dbname='postgres' user='postgres' host='localhost' password='postgres'"

    try:
        conn = psycopg2.connect(login_info)
        conn.set_isolation_level(0)
        cur = conn.cursor()
    except:
        print("I am unable to connect to the database")

    cur.execute("DROP DATABASE IF EXISTS fakebook_db;")
    cur.execute("CREATE DATABASE fakebook_db;")

    return conn, cur


def mode_input(mode_name: str, mode_notes: list) -> None:
    pass
    # '''
    # INSERT INTO Modes(ModeName)
    # '''

if __name__=='__main__':
    main()
