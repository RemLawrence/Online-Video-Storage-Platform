DROP TABLE IF EXISTS videolist;
CREATE TABLE videolist (
  videoListId      INT           NOT NULL AUTO_INCREMENT,
  videoListTitle   VARCHAR(100)  NOT NULL,
  description      VARCHAR(200)  NOT NULL,
  userId           INT           NOT NULL,
  PRIMARY KEY (videoListId),
  FOREIGN KEY (userId) REFERENCES user (userId)
);