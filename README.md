# Fake Book

A "Fake Book" is the sheet music that a jazz musician takes to a performance, containing the essential information on hundreds of standard songs.

## Introduction

There are twelve distinct notes on the piano, but most songs don't use them all. Just as each painting includes some colors and excludes others, each song has its own harmonic palette. My project makes use of relational databases to analyze songs by their harmonic palettes. Note that it is not the notes as such that are relevant; it is their degrees. So instead of an "A minor" chord, we determine the key of the song, and store "iii minor", for instance.

## Data Pipeline

There are a lot of places on the web which list the chords that a performer plays in a given song, because people want to know how to play the song at home (on the guitar, for example). My project scrapes a website to get this information. 

![d](https://i.imgur.com/seeOw5I.png)

## Schema

![d](https://i.imgur.com/O9RbZjd.png)

## Similarity 

Currently the distance function in place between songs is as follows: if song A uses set S of notes, and song B uses set T of notes, then the distance from A to B is the number of elements in the symmetric difference of the sets S and T. 

## Use

The project requires only the `psycopg2`, `beautifulsoup` and `dash` modules.  
