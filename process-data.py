import csv
import psycopg2

def main(MAX_N_TO_PROCESS = None):

    if MAX_N_TO_PROCESS is None:
        print("You did not choose a maximum number of entries to process. It has been automatically set to 500.")
        MAX_N_TO_PROCESS = 500

    with open('/home/Ubuntu/Songbook/key-file.txt') as key_file:
        input_list = key_file.readlines()

    password = input_list[0]

    login_info = "dbname='postgres' user='postgres' host='localhost' password='{}'".format(password)

    try:
        conn = psycopg2.connect(login_info)
        #Look into this more later..."Read committed" and so forth    
        conn.set_isolation_level(0)
    except:
        raise Exception("Problem connecting to the SQL database")

    with open('chords.csv', newline = '') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            # There may be other reasons to skip lines besides this one
            if not row['Chords']:
                continue
            chords_list = row['Chords'].split(',')
            try:
                processed_chords = process_chords(chords_list, row['Key'])
            except:
                print("Something went wrong while parsing the chords of",row['Song Name'],".")
                continue
            id_of_artist = input_artist(conn, row['Artist'])
            id_of_key = note_to_number(row['Key'])
            id_of_song_version, insert_successful = input_song_version(
                conn, 
                row['Song Name'], 
                id_of_artist, 
                id_of_key
            )

            if not insert_successful:
                print("Song version '", row['Song Name'], "' was already in the database.")
                continue
            
            processed_chord_ids = input_chords(conn, processed_chords)
            input_song_version_chords(conn, id_of_song_version, processed_chord_ids)

            # print(id_of_artist)
            # print(chords_list)
            # print(row['Key'])
            # print(processed_chords)

def input_song_version_chords(conn, id_of_song_version, processed_chord_ids):
    cur = conn.cursor()
    # Want to find a way to do this all in one shot, but it's 
    # hard to pass Psycopg2 a variable number of arguments
    for chord_id in processed_chord_ids:        
        SQL = '''INSERT INTO SongVersionChords(SongVersionID, ChordID)
                VALUES
                    (%s, %s)
        '''
        cur.execute(
            SQL,
            (id_of_song_version, chord_id)
        )

def input_chords(conn, processed_chords):
    cur = conn.cursor()
    chord_ids = []
    for chord in processed_chords:
        SQL = '''INSERT INTO Chords(ChordName)
                SELECT %s
                    WHERE NOT EXISTS (
                        SELECT 1 FROM Chords
                        WHERE ChordName = %s
                    ) 
                RETURNING ChordID
        '''
        cur.execute(
            SQL,
            (chord,chord)
        )
        fetch = cur.fetchone()
        if fetch:
            chord_ids.append(fetch[0])
        else:
            SQL2 = '''SELECT ChordID 
                    FROM Chords
                    WHERE ChordName=%s
            '''
            cur.execute(
                SQL2,
                (chord,)
            )
            fetch2 = cur.fetchone()
            if not fetch2:
                raise Exception("The cursor was empty when it shouldn't have been.")
            chord_ids.append(fetch2[0])
    return chord_ids

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

# Returns ID_of_song, true if song was successfully input and ?,false if it was not (if it was already there)
def input_song_version(conn, song_version_name, id_of_artist, id_of_key):
    cur = conn.cursor()
    SQL = '''INSERT INTO SongVersions(SongVersionName, ArtistID, RootToneID)
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

# We encode each absolute note as a number. This is also its AbsoluteNoteID in the Postgres database    
def note_to_number(note_name):
    note_to_number_dict = {
        # Maybe later put lower case or other aliases to make more robust
        'C':1,
        'C#':2,
        'Db':2,
        'D':3,
        'D#':4,
        'Eb':4,
        'E':5,
        'F':6,
        'F#':7,
        'Gb':7,
        'G':8,
        'G#':9,
        'Ab':9,
        'A':10,
        'A#':11,
        'Bb':11,
        'B':12,
        'Cb':12
    }
    return note_to_number_dict[note_name]

def process_chords(chords, song_key):

    number_to_degree = ['I', 'bII', 'II', 'bIII', 'III', 'IV', 'IV#', 'V', 'bVI', 'VI', 'bVII', 'VII']

    res = []
    song_key_numeric = note_to_number(song_key)
    for chord in chords:

        # If our chord comes with a sharp or a flat in the name
        if len(chord)>=2 and (chord[1] == '#' or chord[1] == 'b'):
            chord_root = chord[0:2]
            output_chord_type = chord[2:]
        else:
            chord_root = chord[0]
            output_chord_type = chord[1:]
        output_root_numeric = (note_to_number(chord_root) - song_key_numeric) % 12
        output_root = number_to_degree[output_root_numeric]
        output_chord = output_root + output_chord_type
        res.append(output_chord)
    return res

if __name__=='__main__':
    main()