# INDEXES

USE DbMysql03;

# to drop an index, change the name of the table and the name of the index.
# the neame of indexes used to be the same names as below just without the first word
#ALTER TABLE movies DROP INDEX by_title;



# movies indexes
CREATE INDEX movie_by_title ON DbMysql03.movies (`title`);
CREATE INDEX movie_by_year ON DbMysql03.movies (`year`);
CREATE INDEX movie_by_rating ON DbMysql03.movies (`rating`); 
#CREATE INDEX movie_by_runtime ON DbMysql03.movies (`runtime`); 


# actors indexes
CREATE INDEX actor_by_name ON DbMysql03.actors (`name`);

# directors indexes
CREATE INDEX actor_by_name ON DbMysql03.directors (`name`);


# trailers indexes
CREATE INDEX trailer_by_title ON DbMysql03.trailers (`title`);
CREATE INDEX trailer_by_view_count ON DbMysql03.trailers (`view_count`);
CREATE INDEX trailer_by_likes ON DbMysql03.trailers (`likes`);