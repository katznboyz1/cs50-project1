CREATE TABLE books (
    isbn VARCHAR PRIMARY KEY, /*varchar because some of the values are too large*/
    title VARCHAR NOT NULL,
    title_lowercase VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    author_lowercase VARCHAR NOT NULL,
    year VARCHAR NOT NULL /*also varchar just for consistency*/
);