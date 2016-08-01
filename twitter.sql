DROP TABLE IF EXISTS twitter_user;
CREATE Table twitter_user(
  id serial PRIMARY KEY,
  name varchar NOT NULL UNIQUE
);

DROP TABLE IF EXISTS tweet;
CREATE TABLE tweet(
  id serial PRIMARY KEY,
  message varchar NOT NULL,
  user_id integer NOT NULL REFERENCES twitter_user (id)

);

DROP TABLE IF EXISTS follow;
CREATE TABLE follow(
  id serial PRIMARY KEY,
  follower_id integer NOT NULL REFERENCES twitter_user (id),
  followee_id integer NOT NULL REFERENCES twitter_user (id)
)
