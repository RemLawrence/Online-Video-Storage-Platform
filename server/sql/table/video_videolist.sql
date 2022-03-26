DROP TABLE IF EXISTS video_videolist;
CREATE TABLE video_videolist (
    vv_id INT NOT NULL AUTO_INCREMENT,
    vv_userId VARCHAR(36) NOT NULL,
    vv_videoId VARCHAR(36) NOT NULL,
    vv_videoListId VARCHAR(36) NOT NULL,
    PRIMARY KEY (vv_id),
    FOREIGN KEY (vv_userId) REFERENCES user (userId),
    FOREIGN KEY (vv_videoId) REFERENCES video (videoId),
    FOREIGN KEY (vv_videoListId) REFERENCES videolist (videoListId) 
)