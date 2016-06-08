SELECT selected_movie.title, selected_movie.rating, selected_movie.actor, selected_movie.director,
selected_movie.genre, selected_movie.country, selected_movie.language, trailers.youtube_id, trailers.view_count, trailers.likes
FROM trailers
JOIN (SELECT movies.title, movies.rating, selected_actor.actor, selected_director.director,
		selected_genre.genre, selected_country.country, selected_language.language, movies.movie_id
	FROM movies
    
	JOIN (SELECT actors.name AS actor, movie_actor.movie_id
		FROM actors
		JOIN movie_actor
		ON actors.actor_id = movie_actor.actor_id
		WHERE actors.name = 'Christopher Lee') AS selected_actor
	ON movies.movie_id = selected_actor.movie_id
    
	JOIN (SELECT directors.name AS director, movie_director.movie_id
		FROM directors
		JOIN movie_director
		ON directors.director_id = movie_director.director_id
		WHERE directors.name = 'Terence Fisher') AS selected_director
	ON movies.movie_id = selected_director.movie_id
    
    JOIN (SELECT genres.genre, movie_genre.movie_id
		FROM genres
		JOIN movie_genre
		ON genres.genre_id = movie_genre.genre_id
		WHERE genres.genre = 'Horror') AS selected_genre
	ON movies.movie_id = selected_genre.movie_id
    
    JOIN (SELECT country.country_id, country.country
		FROM country
        WHERE country.country = 'UK') AS selected_country
    ON selected_country.country_id = movies.country_id
    
    JOIN (SELECT language.language_id, language.language
		FROM language
        WHERE language.language = 'English') AS selected_language
    ON selected_language.language_id = movies.language_id
    
    WHERE movies.rating > 6
    ) AS selected_movie
ON trailers.movie_id = selected_movie.movie_id
WHERE trailers.view_count > 20000
GROUP BY selected_movie.movie_id