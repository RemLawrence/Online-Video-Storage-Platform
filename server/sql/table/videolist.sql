DROP TABLE IF EXISTS videolist;
CREATE TABLE videolist (
  videoListId      VARCHAR(36)   NOT NULL,
  videoListTitle   VARCHAR(100)  NOT NULL,
  description      VARCHAR(200)  DEFAULT '',
  userId           VARCHAR(36)   NOT NULL,
  PRIMARY KEY (videoListId),
  FOREIGN KEY (userId) REFERENCES user (userId)
);