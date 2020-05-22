CREATE TABLE users (
    username VARCHAR PRIMARY KEY,
    password VARCHAR NOT NULL,
    password_version VARCHAR NOT NULL
);