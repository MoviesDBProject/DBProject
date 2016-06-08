CREATE OR REPLACE VIEW top_actors AS
SELECT movies.title AS title, trailers.youtube_id AS youtube_id, movies.rating AS rating, actors.name AS name
FROM trailers, movies, movie_actor, actors
WHERE  trailers.movie_id = movies.movie_id AND movies.movie_id = movie_actor.movie_id AND movie_actor.actor_id = actors.actor_id
GROUP BY movies.title