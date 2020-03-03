import csv
from pathlib import Path
import psycopg2
from typing import List, Tuple

def main(MAX_N_TO_PROCESS = None):

    project_folder = Path("/home/ubuntu/Songbook")
    if not project_folder.exists():
        raise Exception('''
        The 'Songbook' directory wasn't where the process-data.py script expected it to be.\
        It can be modified by changing the constructor of project_folder (a pathlib.Path object).
        ''')
    
    chords_file = project_folder / "chords.csv"
    if not chords_file.exists():
        raise Exception
        (
            '''The file 'chords.csv' was not there to be processed by process-data.py.\
            It should be inside the Songbook directory.'''
        )

    _key_file = project_folder / "key-file.txt"
    if not _key_file.exists():
        raise Exception
        (
            '''The process-data module was unable to find the key-file.txt file\
                to log into the postgres database.'''
        )
    
    if MAX_N_TO_PROCESS is None:
        print
        (
            '''You did not choose a maximum number of entries to process.\
                 It has been automatically set to 500.'''
        )
        MAX_N_TO_PROCESS = 500

    with _key_file.open() as key_file:
        input_list = key_file.readlines()

    password = input_list[0]

    login_info = "dbname='postgres' user='postgres' host='localhost' password='{}'".format(password)

    try:
        conn = psycopg2.connect(login_info)
        conn.set_isolation_level(0)
    except:
        raise Exception("Problem connecting to the SQL database")

    with chords_file.open() as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            if not row['Chords']:
                print(row['Song Name'], "did not have any chords in the chords file.")
                continue
            chords_list = row['Chords'].split(',')

            try:
                chords_for_input = process_chords(conn, chords_list, row['Song Key'])
            except:
                print("Something went wrong while parsing the chords of " + row['Song Version Name'] + ".")
                continue

            print("Inputting chords to db")
            print(chords_for_input)
            input_chords(conn, chords_for_input)
#            try:
#                input_chords(conn, chords_for_input)
#            except:
#                print("An error occurred while inputting chords for the song '" + row['Song Version Name'] + "'. The song was skipped.")
#                continue 
            id_of_artist = input_artist(conn, row['Artist Name'])
            id_of_key = note_to_number(row['Song Key'])
            id_of_song_version, insert_successful = input_song_version(
                conn, 
                row['Song Version Name'], 
                id_of_artist, 
                id_of_key
            )

            if not insert_successful:
                print("Song version '", row['Song Version Name'], "' was already in the database.")
                continue
            print("Inputting following song version chords for song", row['Song Version Name'])
            print(chords_for_input)
            input_song_version_chords(conn, id_of_song_version, chords_for_input)

#Input chords inserts items into ChordsByDegree and ChordNoteDegrees (the composite table)
def input_chords(conn, chords_for_input: List[Tuple[int]]) -> None:
    cur = conn.cursor()
    for chord in chords_for_input: 
        root_degree_id = chord[0]
        chord_type_id = chord[1]
        SQL = '''INSERT INTO ChordsByDegree(RootDegreeID, ChordTypeID)
                 SELECT %s, %s
                    WHERE NOT EXISTS(
                        SELECT 1 FROM ChordsByDegree
                        WHERE RootDegreeID = %s
                        AND ChordTypeID = %s
                    )
                RETURNING 1;
              ''' 
        cur.execute(
            SQL,
            (root_degree_id,chord_type_id, root_degree_id, chord_type_id)
        )
        fetch = cur.fetchone()
        #If the chord is already in the database
        if not fetch :
            continue
        SQL2 = '''SELECT ChordTypeShape
                        FROM ChordTypes
                        WHERE ChordTypeId = %s 
                '''
        cur.execute(
            SQL2,
            (chord_type_id,)
        )
        fetch2 = cur.fetchone()
        print("Fetched chord type shape in input...")
        print(fetch2)
        return



def input_song_version_chords(conn, id_of_song_version, chords_for_input):
    cur = conn.cursor()
    for chord in chords_for_input:
        root_degree_id = chord[0]
        chord_type_id = chord[1]
        SQL = '''INSERT INTO SongVersionChords(SongVersionID, RootDegreeID, ChordTypeID)
                VALUES
                    (%s, %s, %s);
        '''
        cur.execute(
            SQL,
            (id_of_song_version, root_degree_id, chord_type_id)
        )



def process_chords(conn, chords, song_key):
    cur = conn.cursor()
    res = []
    song_key_numeric = note_to_number(song_key)
    for chord in chords:

        # If our chord comes with a sharp or a flat in the name
        if len(chord)>=2 and (chord[1] == '#' or chord[1] == 'b'):
            chord_absolute_root = chord[0:2]
            chord_type = chord[2:]
        else:
            chord_absolute_root = chord[0]
            chord_type = chord[1:]
        root_degree_id = (note_to_number(chord_absolute_root) - song_key_numeric) % 12
        SQL = '''SELECT ChordTypeID
                     FROM ChordTypes
                     WHERE ChordTypeName = %s;
              ''' 
        cur.execute(
            SQL,
            (chord_type,)
        )
        fetch = cur.fetchone()
        if not fetch:
            print("The chord type", chord_type, "was not found in the ChordTypes table.")
            raise Exception()
        chord_type_id = fetch[0] 
        res.append((root_degree_id, chord_type_id))
    return res

# Returns ArtistID of new row (or ArtistID of row which already existed)
def input_artist(conn, artist_name):
    cur = conn.cursor()
    SQL = '''INSERT INTO Artists(ArtistName)
            SELECT %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM Artists
                    WHERE ArtistName = %s
                )
            RETURNING ArtistID;
    '''
    cur.execute(
        SQL,
        (artist_name, artist_name)
    )
    fetch = cur.fetchone()
    if fetch:
        id_of_new_row = fetch[0]
        return id_of_new_row
    else:
        SQL2 = '''SELECT ArtistID
                FROM Artists
                WHERE ArtistName = %s
        '''
        cur.execute(
            SQL2,
            (artist_name,)
        )
        fetch2 = cur.fetchone()
        if not fetch2:
            raise Exception("The cursor was empty when it shouldn't have been.")
        return fetch2[0]

# Returns ID_of_song, true if song was successfully input and -1,false if it was not (if it was already there)
def input_song_version(conn, song_version_name, id_of_artist, id_of_key):
    cur = conn.cursor()
    SQL = '''INSERT INTO SongVersions(SongVersionName, ArtistID, RootAbsoluteNoteID)
            SELECT %s, %s, %s
                WHERE NOT EXISTS(
                    SELECT 1 FROM SongVersions
                    WHERE SongVersionName = %s
                )
            RETURNING SongVersionID;
    '''
    cur.execute(
        SQL,
        (song_version_name, id_of_artist, id_of_key, song_version_name)
    )
    fetch = cur.fetchone()
    if not fetch:
        return -1, False
    return fetch[0], True

# # We encode each absolute note as a number. This is also its AbsoluteNoteID in the Postgres database    
def note_to_number(note_name):
    note_to_number_dict = {
        'C':0,
        'C#':1,
        'Db':1,
        'D':2,
        'D#':3,
        'Eb':3,
        'E':4,
        'F':5,
        'F#':6,
        'Gb':6,
        'G':7,
        'G#':8,
        'Ab':8,
        'A':9,
        'A#':10,
        'Bb':10,
        'B':11,
        'Cb':11
    }
    return note_to_number_dict[note_name]

if __name__=='__main__':
    main()
