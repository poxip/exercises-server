DROP TABLE IF EXISTS questions;
CREATE TABLE questions (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  title    TEXT NOT NULL,
  content  TEXT NOT NULL,
  solution TEXT NOT NULL
);