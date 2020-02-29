#!/usr/bin/python3
#

import psycopg2

def main():

    with open('/home/Ubuntu/Songbook/key-file.txt') as key_file:
        input_list = key_file.readlines()

    password = input_list[0]

    login_info = "dbname='postgres' user='postgres' host='localhost' password='{}'".format(password)

    SQL = """
    CREATE TABLE TimePeriods (
        TimePeriodID INT GENERATED BY DEFAULT AS IDENTITY,
        TimePeriodName CHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (TimePeriodID)
    );

    CREATE TABLE Genres (
        GenreID SMALLINT GENERATED BY DEFAULT AS IDENTITY,
        GenreName CHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY(GenreID)
    );

    CREATE TABLE Modes(
        ModeID SMALLINT GENERATED BY DEFAULT AS IDENTITY,
        ModeName CHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (ModeID)
    );

    CREATE TABLE AbsoluteNotes(
        AbsoluteNoteID SMALLINT,
        AbsoluteNoteName CHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (AbsoluteNoteID)
    );

    CREATE TABLE NoteDegrees(
        NoteDegreeID SMALLINT GENERATED BY DEFAULT AS IDENTITY,
        NoteDegreeName CHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (NoteDegreeID)
    );

    CREATE TABLE ChordTypes(
        ChordTypeID SMALLINT GENERATED BY DEFAULT AS IDENTITY,
        ChordName CHAR(50) UNIQUE NOT NULL,
        ChordShape CHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (ChordTypeID)
    )
    
    CREATE TABLE PopularityLevels(
        PopularityLevelID SMALLINT GENERATED BY DEFAULT AS IDENTITY,
        PopularityLevelName CHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (PopularityLevelID)
    );

    CREATE TABLE Artists(
        ArtistID BIGINT GENERATED BY DEFAULT AS IDENTITY,
        ArtistName CHAR(50) NOT NULL,
        PRIMARY KEY (ArtistID)
    );

    CREATE TABLE ModeNoteDegrees(
        ModeID SMALLINT,
        NoteDegreeID SMALLINT,
        PRIMARY KEY (ModeID, NoteDegreeID),
        FOREIGN KEY (ModeID) REFERENCES Modes(ModeID),
        FOREIGN KEY (NoteDegreeID) REFERENCES NoteDegrees(NoteDegreeID)
    );

    CREATE TABLE ChordsByDegree(
        RootDegreeID SMALLINT,
        ChordTypeID SMALLINT,
        PRIMARY KEY (RootDegreeID, ChordTypeID),
        FOREIGN KEY (RootDegreeID) REFERENCES NoteDegrees(NoteDegreeID),
        FOREIGN KEY (ChordTypeID) REFERENCES ChordTypes(ChordTypeID)
    );

    CREATE TABLE ChordNoteDegrees(
        RootDegreeID SMALLINT,
        ChordTypeID SMALLINT,
        NoteDegreeID SMALLINT
        PRIMARY KEY (RootDegreeID, ChordTypeID, NoteDegreeID),
        FOREIGN KEY (RootDegreeID, ChordTypeID) REFERENCES ChordsByDegree(RootDegreeID, ChordTypeID),
        FOREIGN KEY (NoteDegreeID) REFERENCES NoteDegrees(NoteDegreeID)
    );

    CREATE TABLE SongVersions(
        SongVersionID BIGINT GENERATED BY DEFAULT AS IDENTITY,
        SongVersionName CHAR(50) NOT NULL,
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

    CREATE TABLE SongVersionChords(
        SongVersionID BIGINT,
        ChordID SMALLINT,
        PRIMARY KEY (SongVersionID, ChordID),
        FOREIGN KEY (SongVersionID) REFERENCES SongVersions(SongVersionID),
        FOREIGN KEY (ChordID) REFERENCES Chords(ChordID)
    );

    CREATE TABLE SongVersionGenres(
        SongVersionID BIGINT,
        GenreID SMALLINT,
        PRIMARY KEY (SongVersionID, GenreID),
        FOREIGN KEY (SongVersionID) REFERENCES SongVersions(SongVersionID),
        FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
    );

    INSERT INTO AbsoluteNotes(AbsoluteNoteName, AbsoluteNoteID)
    VALUES
        ('C', 1),
        ('C#', 2),
        ('Db', 2),
        ('D', 3),
        ('D#', 4),
        ('Eb', 4),
        ('E', 5),
        ('E#', 6),
        ('F', 6),
        ('F#', 7),
        ('Gb', 7),
        ('G', 8),
        ('G#', 9),
        ('Ab', 9),
        ('A', 10),
        ('A#', 11),
        ('Bb', 11),
        ('B', 12),
        ('Cb', 12);
    
    INSERT INTO ChordTypes(ChordName, ChordShape)
    VALUES
        ("", "0,4,3")
        ("m", "0,3,4")
    """

    # INSERT INTO ChordNoteDegrees()

    # INSERT INTO Modes()

    try:
        conn = psycopg2.connect(login_info)
        conn.set_isolation_level(0)
        cur = conn.cursor()
        cur.execute(SQL)
    except:
        print("I am unable to connect to the database")

    # INSERT INTO ChordNoteDegrees()

    # INSERT INTO Modes()

# Make function to input a mode into the 
def mode_input(mode_name: str, mode_notes: list) -> None:
    pass
    # '''
    # INSERT INTO Modes(ModeName)
    # '''

if __name__=='__main__':
    main()