CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    movie TEXT, 
    rating INTEGER, 
    review TEXT
);

CREATE TABLE movie_info (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES reviews,
    genre TEXT,
    director TEXT,
    year INTEGER
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES reviews,
    user_id INTEGER REFERENCES users,
    content TEXT
);
