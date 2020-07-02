time_periods_table_create = """
    CREATE TABLE TimePeriods (
        TimePeriodID SERIAL NOT NULL,
        TimePeriodName VARCHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (TimePeriodID)
    );
    """

genres_table_create = """
    CREATE TABLE Genres (
        GenreID SERIAL NOT NULL,
        GenreName VARCHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY(GenreID)
    );
"""

modes_table_create = """
    CREATE TABLE Modes(
        ModeID SERIAL NOT NULL,
        ModeName VARCHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (ModeID)
    );
"""

absolute_notes_table_create = """
    CREATE TABLE AbsoluteNotes(
        AbsoluteNoteID SMALLINT,
        PRIMARY KEY (AbsoluteNoteID)
    );
"""

absolute_note_names_table_create = """
    CREATE TABLE AbsoluteNoteNames(
        AbsoluteNoteNameID SERIAL NOT NULL,
        AbsoluteNoteName VARCHAR(2) UNIQUE NOT NULL,
        AbsoluteNoteID SMALLINT,
        PRIMARY KEY (AbsoluteNoteNameID),
        FOREIGN KEY (AbsoluteNoteID) REFERENCES AbsoluteNotes(AbsoluteNoteID)
    );
"""

note_degrees_table_create = """
    CREATE TABLE NoteDegrees(
        NoteDegreeID SERIAL NOT NULL,
        NoteDegreeName VARCHAR(5) UNIQUE NOT NULL,
        PRIMARY KEY (NoteDegreeID)
    );
"""

chord_types_table_create = """
    CREATE TABLE ChordTypes(
        ChordTypeID SERIAL NOT NULL,
        ChordTypeName VARCHAR(50) UNIQUE NOT NULL,
        ChordTypeShape VARCHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (ChordTypeID)
    );
"""

popularity_levels_table_create = """
    CREATE TABLE PopularityLevels(
        PopularityLevelID SERIAL NOT NULL,
        PopularityLevelName VARCHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (PopularityLevelID)
    );
"""

artists_table_create = """
    CREATE TABLE Artists(
        ArtistID BIGSERIAL NOT NULL,
        ArtistName VARCHAR(50) NOT NULL,
        PRIMARY KEY (ArtistID)
    );
"""

mode_note_degrees_table_create = """
    CREATE TABLE ModeNoteDegrees(
        ModeID SMALLINT,
        NoteDegreeID SMALLINT,
        PRIMARY KEY (ModeID, NoteDegreeID),
        FOREIGN KEY (ModeID) REFERENCES Modes(ModeID),
        FOREIGN KEY (NoteDegreeID) REFERENCES NoteDegrees(NoteDegreeID)
    );
"""

chords_by_degree_table_create = """
    CREATE TABLE ChordsByDegree(
        RootDegreeID SMALLINT,
        ChordTypeID SMALLINT,
        PRIMARY KEY (RootDegreeID, ChordTypeID),
        FOREIGN KEY (RootDegreeID) REFERENCES NoteDegrees(NoteDegreeID),
        FOREIGN KEY (ChordTypeID) REFERENCES ChordTypes(ChordTypeID)
    );
"""

chord_note_degrees_table_create = """
    CREATE TABLE ChordNoteDegrees(
        RootDegreeID SMALLINT,
        ChordTypeID SMALLINT,
        NoteDegreeID SMALLINT,
        PRIMARY KEY (RootDegreeID, ChordTypeID, NoteDegreeID),
        FOREIGN KEY (RootDegreeID, ChordTypeID) REFERENCES ChordsByDegree(RootDegreeID, ChordTypeID),
        FOREIGN KEY (NoteDegreeID) REFERENCES NoteDegrees(NoteDegreeID)
    );
"""

song_versions_table_create = """
    CREATE TABLE SongVersions(
        SongVersionID BIGSERIAL NOT NULL,
        SongVersionName VARCHAR(50) NOT NULL,
        ArtistID BIGINT NOT NULL,
        RootAbsoluteNoteID SMALLINT NOT NULL,
        PopularityLevelID SMALLINT, 
        TimePeriodID INT,
        PRIMARY KEY (SongVersionID),
        FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID),
        FOREIGN KEY (RootAbsoluteNoteID) REFERENCES AbsoluteNotes(AbsoluteNoteID),
        FOREIGN KEY (PopularityLevelID) REFERENCES PopularityLevels(PopularityLevelID),
        FOREIGN KEY (TimePeriodID) REFERENCES TimePeriods(TimePeriodID)
    );
"""

song_version_chords_table_create = """
    CREATE TABLE SongVersionChords(
        SongVersionID BIGINT,
        RootDegreeID SMALLINT,
        ChordTypeID SMALLINT,
        PRIMARY KEY (SongVersionID, RootDegreeID, ChordTypeID),
        FOREIGN KEY (SongVersionID) REFERENCES SongVersions(SongVersionID),
        FOREIGN KEY (RootDegreeID, ChordTypeID) REFERENCES ChordsByDegree(RootDegreeID, ChordTypeID)
    );
"""

song_version_genres_table_create = """
    CREATE TABLE SongVersionGenres(
        SongVersionID BIGINT,
        GenreID SMALLINT,
        PRIMARY KEY (SongVersionID, GenreID),
        FOREIGN KEY (SongVersionID) REFERENCES SongVersions(SongVersionID),
        FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
    );
"""

song_version_pairs_table_create = """
    CREATE TABLE SongVersionPairs(
        SongVersionID1 BIGINT,
        SongVersionID2 BIGINT,
        Distance NUMERIC,
        PRIMARY KEY (SongVersionID1, SongVersionID2),
        FOREIGN KEY (SongVersionID1) REFERENCES SongVersions(SongVersionID),
        FOREIGN KEY (SongVersionID2) REFERENCES SongVersions(SongVersionID),
        CHECK (SongVersionID1 <= SongVersionID2)
    );
"""

absolute_notes_table_insert = """
    INSERT INTO AbsoluteNotes(AbsoluteNoteID)
    VALUES
        (0), 
        (1),
        (2),
        (3),
        (4),
        (5),
        (6),
        (7),
        (8),
        (9),
        (10),
        (11);
"""

absolute_note_names_table_insert = """
    INSERT INTO AbsoluteNoteNames(AbsoluteNoteName, AbsoluteNoteID)
    VALUES
        ('C', 0),
        ('C#', 1),
        ('Db', 1),
        ('D', 2),
        ('D#', 3),
        ('Eb', 3),
        ('E', 4),
        ('E#', 5),
        ('F', 5),
        ('F#', 6),
        ('Gb', 6),
        ('G', 7),
        ('G#', 8),
        ('Ab', 8),
        ('A', 9),
        ('A#', 10),
        ('Bb', 10),
        ('B', 11),
        ('Cb', 11);
"""

note_degrees_table_insert = """
    INSERT INTO NoteDegrees(NoteDegreeID, NoteDegreeName)
    VALUES
        (0, 'I'),
        (1, 'bII'),
        (2, 'II'),
        (3, 'bIII'),
        (4, 'III'),
        (5, 'IV'),
        (6, '#IV'),
        (7, 'V'),
        (8, 'bVI'),
        (9, 'VI'),
        (10, 'bVII'),
        (11, 'VII');
"""

chord_types_table_insert = """
    INSERT INTO ChordTypes(ChordTypeName, ChordTypeShape)
    VALUES
        ('', '0,4,3'),
        ('m', '0,3,4'),
        ('5', '0,7'),
    	('7', '0,4,3,3');
"""

modes_table_insert = """
    INSERT INTO Modes(ModeID, ModeName)
    VALUES
        (1, 'Ionian'),
        (2, 'Dorian'),
        (3, 'Phrygian'),
        (4, 'Lydian'),
        (5, 'Mixolydian'),
        (6, 'Aeolian'),
        (7, 'Locrian');
"""

mode_note_degrees_table_insert = """
    INSERT INTO ModeNoteDegrees(ModeID, NoteDegreeID)
    VALUES
        (1, 0),(1, 2),(1, 4),(1, 5),(1, 7),(1, 9),(1, 11),
        (2, 0),(2, 2),(2, 3),(2, 5),(2, 7),(2, 9),(2, 10),
        (3, 0),(3, 1),(3, 3),(3, 5),(3, 7),(3, 8),(3, 10),
        (4, 0),(4, 2),(4, 4),(4, 6),(4, 7),(4, 9),(4, 11),
        (5, 0),(5, 2),(5, 4),(5, 5),(5, 7),(5, 9),(5, 10),
        (6, 0),(6, 2),(6, 3),(6, 5),(6, 7),(6, 8),(6, 10),
        (7, 0),(7, 1),(7, 3),(7, 5),(7, 6),(7, 8),(7, 10);
"""

# Query lists

create_table_queries = [time_periods_table_create, 
                        genres_table_create, 
                        modes_table_create, 
                        absolute_notes_table_create, 
                        absolute_note_names_table_create, 
                        note_degrees_table_create, 
                        chord_types_table_create, 
                        popularity_levels_table_create, 
                        artists_table_create, 
                        mode_note_degrees_table_create, 
                        chords_by_degree_table_create, 
                        chord_note_degrees_table_create, 
                        song_versions_table_create, 
                        song_version_chords_table_create,
                        song_version_genres_table_create,
                        song_version_pairs_table_create]

insert_table_queries = [absolute_notes_table_insert,
                        absolute_note_names_table_insert,
                        note_degrees_table_insert,
                        chord_types_table_insert,
                        modes_table_insert,
                        mode_note_degrees_table_insert]