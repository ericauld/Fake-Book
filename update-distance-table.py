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

    update_distance(conn, [1, 2])
    return 
    
    SQL = '''Select sv1.SongVersionID, sv2.SongVersionID
                From 
                    SongVersions sv1,
	                SongVersions sv2
                Where sv1.SongVersionID <= sv2.SongVersionID;
    '''

    cur = conn.cursor()
    cur.execute(SQL)
    song_id_pairs = cur.fetchall()
    cur.close()

    for song_id_pair in song_id_pairs:
        update_distance(conn, song_id_pair)

def update_distance(conn, song_id_pair):
    cur = conn.cursor()
    song_id_1 = song_id_pair[0]
    song_id_2 = song_id_pair[1]
    SQL1 = '''SELECT DISTINCT chordnot.NoteDegreeID as NoteID
                FROM 
                    SongVersions ver
                    INNER JOIN SongVersionChords verch
                        ON ver.SongVersionID = verch.SongVersionID
                    INNER JOIN ChordNoteDegrees chordnot
                        ON 
                            chordnot.RootDegreeID = verch.RootDegreeID
                            AND chordnot.ChordTypeID = verch.ChordTypeID
                WHERE ver.SongVersionID = %s
            ORDER BY chordnot.NoteDegreeID;
        '''
    cur.execute(
        SQL1,
        (song_id_1,)
    )
    notes_1 = cur.fetchall()

    SQL2 = '''SELECT DISTINCT chordnot.NoteDegreeID as NoteID
                FROM 
                    SongVersions ver
                    INNER JOIN SongVersionChords verch
                        ON ver.SongVersionID = verch.SongVersionID
                    INNER JOIN ChordNoteDegrees chordnot
                        ON 
                            chordnot.RootDegreeID = verch.RootDegreeID
                            AND chordnot.ChordTypeID = verch.ChordTypeID
                WHERE ver.SongVersionID = %s
            ORDER BY chordnot.NoteDegreeID;
        '''
    cur.execute(
        SQL2,
        (song_id_2,)
    )
    notes_2 = cur.fetchall()

    print(notes_1, notes_2)
    



if __name__=='__main__':
    main()
