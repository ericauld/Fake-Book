#!/usr/bin/python3
#

import psycopg2
from pathlib import Path

def main():

    project_folder = Path("/home/ubuntu/Songbook")
    _key_file = project_folder / "key-file.txt"

    with _key_file.open() as key_file:
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
        PRIMARY KEY (AbsoluteNoteID)
    );
    
    CREATE TABLE AbsoluteNoteNames(
        AbsoluteNoteNameID SMALLINT GENERATED BY DEFAULT AS IDENTITY,
        AbsoluteNoteName CHAR(50) UNIQUE NOT NULL,
        AbsoluteNoteID SMALLINT,
        PRIMARY KEY (AbsoluteNoteNameID),
        FOREIGN KEY (AbsoluteNoteID) REFERENCES AbsoluteNotes(AbsoluteNoteID)
    );

    CREATE TABLE NoteDegrees(
        NoteDegreeID SMALLINT GENERATED BY DEFAULT AS IDENTITY,
        NoteDegreeName CHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (NoteDegreeID)
    );

    CREATE TABLE ChordTypes(
        ChordTypeID SMALLINT GENERATED BY DEFAULT AS IDENTITY,
        ChordTypeName CHAR(50) UNIQUE NOT NULL,
        ChordTypeShape CHAR(50) UNIQUE NOT NULL,
        PRIMARY KEY (ChordTypeID)
    );
    
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
        NoteDegreeID SMALLINT,
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
        RootDegreeID SMALLINT,
        ChordTypeID SMALLINT,
        PRIMARY KEY (SongVersionID, RootDegreeID, ChordTypeID),
        FOREIGN KEY (SongVersionID) REFERENCES SongVersions(SongVersionID),
        FOREIGN KEY (RootDegreeID, ChordTypeID) REFERENCES ChordsByDegree(RootDegreeID, ChordTypeID)
    );

    CREATE TABLE SongVersionGenres(
        SongVersionID BIGINT,
        GenreID SMALLINT,
        PRIMARY KEY (SongVersionID, GenreID),
        FOREIGN KEY (SongVersionID) REFERENCES SongVersions(SongVersionID),
        FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
    );

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
    
    INSERT INTO ChordTypes(ChordTypeName, ChordTypeShape)
    VALUES
        ('', '0,4,3'),
        ('m', '0,3,4'),
        ('5', '0,7'),
    	('7', '0,4,3,3');
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

def mode_input(mode_name: str, mode_notes: list) -> None:
    pass
    # '''
    # INSERT INTO Modes(ModeName)
    # '''

if __name__=='__main__':
    main()
