import psycopg2
from pathlib import Path

def main():
    project_folder = Path("/home/ubuntu/Songbook")
    _key_file = project_folder / "key-file.txt"

    with _key_file.open() as key_file:
        input_list = key_file.readlines()

    password = input_list[0]
    login_info = "dbname='postgres' user='postgres' host='localhost' password='{}'".format(password)

    try:
        conn = psycopg2.connect(login_info)
        conn.set_isolation_level(0)
    except:
        print("I am unable to connect to the database")

    SQL = '''Select sv1.SongVersionName, sv2.SongVersionName
                From 
                    SongVersions sv1,
	                SongVersions sv2
                Where sv1.SongVersionName < sv2.SongVersionName
    '''

    cur = conn.cursor()
    cur.execute(SQL)
    print(cur.fetchone())
    print(cur.fetchone())
    print(cur.fetchall())

if __name__=='__main__':
    main()