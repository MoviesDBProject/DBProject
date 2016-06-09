

USE DbMysql03;

# TABLES:

# country
CREATE TABLE IF NOT EXISTS DbMysql03.country (
  country_id INT NOT NULL,
  country VARCHAR(50) NOT NULL,
  
  PRIMARY KEY (country_id)
  )ENGINE=INNODB;
  
  
# language
CREATE TABLE IF NOT EXISTS DbMysql03.language (
  language_id INT NOT NULL,
  language VARCHAR(50) NOT NULL,
  
  PRIMARY KEY (language_id)
  )ENGINE=INNODB;
  


# genres
CREATE TABLE IF NOT EXISTS DbMysql03.genres (
  genre_id INT NOT NULL,
  genre VARCHAR(50) NOT NULL,
  
  PRIMARY KEY (genre_id)
  )ENGINE=INNODB;



# movies
CREATE TABLE IF NOT EXISTS DbMysql03.movies (
  movie_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  year INT,
  country_id INT,
  language_id INT,
  rating DECIMAL(2,1),
  runtime INT,
  #description VARCHAR(20),
  
  PRIMARY KEY (movie_id),
  
  FOREIGN KEY (language_id)
		REFERENCES language(language_id),
        
  FOREIGN KEY (country_id)
		REFERENCES country(country_id)
  )ENGINE=INNODB;
  
  
  
# movie_genre
CREATE TABLE IF NOT EXISTS DbMysql03.movie_genre (
  genre_id INT NOT NULL,
  movie_id INT NOT NULL,

  PRIMARY KEY (genre_id, movie_id),
        
  FOREIGN KEY (genre_id)
		REFERENCES genres(genre_id),
  FOREIGN KEY (movie_id)
		REFERENCES movies(movie_id)
  )ENGINE=INNODB;
  
  
# actors
CREATE TABLE IF NOT EXISTS DbMysql03.actors (
  actor_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,

  PRIMARY KEY (actor_id)
        
  )ENGINE=INNODB;


# movie_actor
CREATE TABLE IF NOT EXISTS DbMysql03.movie_actor (
  actor_id INT NOT NULL,
  movie_id INT NOT NULL,

  PRIMARY KEY (actor_id, movie_id),
        
  FOREIGN KEY (actor_id)
		REFERENCES actors(actor_id),
  FOREIGN KEY (movie_id)
		REFERENCES movies(movie_id)
  )ENGINE=INNODB;
  
  

# directors
CREATE TABLE IF NOT EXISTS DbMysql03.directors (
  director_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  

  PRIMARY KEY (director_id)
	
  )ENGINE=INNODB;
  
  
# movie_director
CREATE TABLE IF NOT EXISTS DbMysql03.movie_director (
  director_id INT NOT NULL,
  movie_id INT NOT NULL,

  PRIMARY KEY (director_id, movie_id),
        
  FOREIGN KEY (director_id)
		REFERENCES directors(director_id),
  FOREIGN KEY (movie_id)
		REFERENCES movies(movie_id)
  )ENGINE=INNODB;
  
  
  
# trailers
CREATE TABLE IF NOT EXISTS DbMysql03.trailers (
  trailer_id INT NOT NULL,
  youtube_id VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  movie_id INT NOT NULL,
  view_count INT NOT NULL,
  likes INT NOT NULL,
  
  PRIMARY KEY (trailer_id),
  
  FOREIGN KEY (movie_id)
		REFERENCES movies(movie_id)
        
  )ENGINE=INNODB;
  
