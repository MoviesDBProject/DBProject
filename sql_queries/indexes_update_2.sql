# INDEXES

USE DbMysql03;

# to drop an index, change the name of the table and the name of the index.
# the neame of indexes used to be the same names as below just without the first word
#ALTER TABLE movies DROP INDEX by_title;



# movies indexes
ALTER TABLE movies ADD INDEX movie_by_title ON (title)
ALTER TABLE movies ADD INDEX movie_by_year ON (year)
ALTER TABLE movies ADD INDEX movie_by_rating ON (rating)


# actors indexes
ALTER TABLE actors ADD INDEX actor_by_name ON (name)

# directors indexes
ALTER TABLE directors ADD INDEX director_by_name ON (name)


# trailers indexes
ALTER TABLE trailers ADD INDEX trailer_by_title ON (title)
ALTER TABLE trailers ADD INDEX trailer_by_view_count ON (view_count)
ALTER TABLE trailers ADD INDEX trailer_by_likes ON (likes)