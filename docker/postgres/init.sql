CREATE TABLE IF NOT EXISTS albums (
    id varchar(255) primary key,
    artist varchar(255) not null,
    name varchar(255) not null,
    release_date date not null,
    total_track int
);

CREATE TABLE IF NOT EXISTS artists (
    id varchar(255) primary key,
    name varchar(255) not null
);

CREATE TABLE IF NOT EXISTS album_artists (
    id varchar(255) primary key,
    artist_id varchar(255) references artists(id),
    album_id varchar(255) references albums(id)
);