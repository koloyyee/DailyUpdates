DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS news;
DROP TABLE IF EXISTS agency;


CREATE TABLE agency
(
    id SERIAL PRIMARY KEY,
    agency VARCHAR (50) UNIQUE NOT NULL,
    url VARCHAR (255) NOT NULL
);
CREATE TABLE news
(
    id SERIAL PRIMARY KEY,
    headline VARCHAR (255) NOT NULL,
    url TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    agency_id INTEGER NOT NULL,
    FOREIGN KEY
(agency_id) REFERENCES agency
(id)
);
CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username VARCHAR (50) UNIQUE NOT NULL,
    password VARCHAR (125) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE post
(
    id SERIAL PRIMARY KEY,
    author_id INT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR (255) NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY
(author_id) REFERENCES users
(id)
);