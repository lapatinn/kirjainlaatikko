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

