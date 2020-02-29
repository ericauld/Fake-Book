# Songbook

There are twelve distinct notes on the piano, but most songs don't use them all. Just as each painting includes some colors and excludes others, each song has its own harmonic palette. My project makes use of relational databases to analyze songs by their harmonic palettes. 

## Data Pipeline

There are a lot of places on the web which list the chords which appear in a given song, because people want to know how to play the song, on the guitar, for example. My project scrapes a website to get this information. 

![d](https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRx_2P10P63OkW1HP0IPmtpAfv5Uw9Uu8Xm75Mye7KpzeZtcFa2)

![d](https://halcyoona.files.wordpress.com/2018/07/ec2-logo.png)

![d](https://blog.desdelinux.net/wp-content/uploads/2018/10/postgresql.jpeg)

## What is a "Mode"?

In music theory, a __mode__ is a subset of the twelve available notes -- a subset popular enough to be known by name. (For example, the Mixolydian mode consists of {1, 2, 3, 4, 5, 6, b7}.) Using my interface, one can pick a mode and see which songs in the database use that mode, or which use a close relative.

Notice that we use numbers instead of letters.  

## Similarity 



## Use

If you want to insert your own modes, you can use `setup-schema.mode_input`. You can then search for songs which the database finds to be closest to that mode. One can find a number of examples on ![d](https://en.wikipedia.org/wiki/Mode_(music)#Other_types). 