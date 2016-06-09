

# INDEXES

# movies indexes
CREATE INDEX by_title ON DbMysql03.movies ('title');
CREATE INDEX by_year ON DbMysql03.movies ('year');
CREATE INDEX by_rating ON DbMysql03.movies ('rating'); 
#CREATE INDEX by_runtime ON DbMysql03.movies ('runtime'); 


# actors indexes
CREATE INDEX by_name ON DbMysql03.actors ('name');

# directors indexes
CREATE INDEX by_name ON DbMysql03.directors ('title');


# trailers indexes
CREATE INDEX by_title ON DbMysql03.trailers ('title');
CREATE INDEX by_view_count ON DbMysql03.trailers ('view_count');
CREATE INDEX by_likes ON DbMysql03.trailers ('likes');