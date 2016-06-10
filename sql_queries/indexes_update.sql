# INDEXES

USE DbMysql03;


# movies indexes
ALTER TABLE movies ADD INDEX movie_by_title (title) USING HASH
ALTER TABLE movies ADD INDEX movie_by_year (year)
ALTER TABLE movies ADD INDEX movie_by_rating (rating)


# actors indexes
ALTER TABLE actors ADD INDEX actor_by_name (name) USING HASH

# directors indexes
ALTER TABLE directors ADD INDEX director_by_name (name) USING HASH


# trailers indexes
ALTER TABLE trailers ADD INDEX trailer_by_title (title) USING HASH
ALTER TABLE trailers ADD INDEX trailer_by_view_count (view_count)
ALTER TABLE trailers ADD INDEX trailer_by_likes (likes)