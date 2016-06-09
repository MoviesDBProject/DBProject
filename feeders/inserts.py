import MySQLdb
from dbpedia_feeder import *
from pycountry import *




def actors_insert(actors_table):
    conn = MySQLdb.connect(host="mysqlsrv.cs.tau.ac.il",
                           user="DbMysql03",
                           passwd="DbMysql03",
                           db="DbMysql03")

    cursor = conn.cursor()

    for actor in actors_table:
        try:
            actor_id = actor[ID.lower()]
            actor_name = actor[NAME.lower()]


            ############################ ACTOR INSERTS  ###############################################
            # insert actor data
            cursor.execute("""
                INSERT INTO actors
                    (actor_id, name)
                VALUES
                   (%s, %s)
               ON DUPLICATE KEY UPDATE
                                                 -- no need to update the PK
                   actor_id  = VALUES(actor_id),
                   name   = VALUES(name);
                          """, (actor_id, actor_name)  # python variables
                           )

        except Exception as e:
            print e

    cursor.execute(""" SELECT * FROM actors """)
    data = cursor.fetchall()
    for row in data:
        print row[0], row[1]


    conn.close()




def directors_insert(directors_table):
    conn = MySQLdb.connect(host="mysqlsrv.cs.tau.ac.il",
                           user="DbMysql03",
                           passwd="DbMysql03",
                           db="DbMysql03")

    cursor = conn.cursor()

    for director in directors_table:
        try:
            director_id = director[ID.tolower()]
            director_name = director[NAME.tolower()]

            ############################ DIRECTOR INSERTS  ###############################################
            # insert director data
            cursor.execute("""
                INSERT INTO directors
                    (director_id, name)
                VALUES
                   (%s, %s)
               ON DUPLICATE KEY UPDATE
                                                 -- no need to update the PK
                   director_id  = VALUES(director_id),
                   name   = VALUES(name);
                          """, (director_id, director_name)  # python variables
                           )

        except Exception as e:
            print e

    conn.close()





def movies_insert(movies_table):
    conn = MySQLdb.connect(host="mysqlsrv.cs.tau.ac.il",
                           user="DbMysql03",
                           passwd="DbMysql03",
                           db="DbMysql03")

    cursor = conn.cursor()

    for movie in movies_table:
        try:

            movie_actors = movie[ACTORS.tolower()]
            movie_directors = movie[DIRECTORS.tolower()]

            movie_id = movie[ID.tolower()]
            movie_name = movie[NAME.tolower()]
            movie_year = movie[OMDB_YEAR.tolower()]
            movie_genres = movie[OMDB_GENRE.tolower()] # a list of genres
            movie_rating = movie[OMDB_IMDB_RATING.tolower()]
            movie_language = movie[OMDB_LANGUAGE.tolower()]
            movie_runtime = movie[OMDB_RUNTIME.tolower()]
            youtube_id =  movie[YOUTUBE.tolower()]['id']
            youtube_title = movie[YOUTUBE.tolower()]['title']
            youtube_view_count = movie[YOUTUBE.tolower()]['view_count']
            youtube_likes = movie[YOUTUBE.tolower()]['likes']



            for genre in movie_genres:
                if genre != 'N/A':
                    ############################ GENRE INSERTS  ###############################################
                    # insert genre
                    cursor.execute("""
                        INSERT INTO genre
                            (genre)
                        VALUES
                           (%s)
                       ON DUPLICATE KEY UPDATE
                                                         -- no need to update the PK
                           genre  = VALUES(genre);
                                  """, (genre)  # python variables
                                   )



            if movie_language != 'N/A':
                ############################ LANGUAGE INSERTS  ###############################################
                # insert language
                cursor.execute("""
                    INSERT INTO language
                        (language)
                    VALUES
                       (%s)
                   ON DUPLICATE KEY UPDATE
                                                     -- no need to update the PK
                       language  = VALUES(language);
                              """, (movie_language)  # python variables
                               )

            if movie[COUNTRY.tolower()] != 'N/A':
                movie_country = movie[COUNTRY].rsplit(',', 1)[1].lstrip()
                movie_country_id = countries[movie_country]

                ############################ COUNTRY INSERTS  ###############################################
                # insert movie country
                cursor.execute("""
                    INSERT INTO country
                        (country_id, country)
                    VALUES
                       (%s, %s)
                   ON DUPLICATE KEY UPDATE
                                                     -- no need to update the PK
                       country_id  = VALUES(country_id),
                       country   = VALUES(country) ;
                              """, (movie_country_id, movie_country)  # python variables
                               )
            else:
                movie_country_id = ''





            ############################ MOVIE INSERTS  ###############################################
            # insert movie data
            cursor.execute("""
                INSERT INTO movies
                    (movie_id, title, year, country_id, language_id, rating, runtime)
                VALUES
                   (%s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE
                                                 -- no need to update the PK
                   movie_id  = VALUES(movie_id),
                   title   = VALUES(title),
                   year  = VALUES(year),
                   country_id  = VALUES(country_id),
                   language_id  = VALUES(language_id),
                   genre  = VALUES(genre),
                   rating  = VALUES(rating),
                   runtime  = VALUES(runtime);
                          """, (movie_id, movie_name, movie_year, movie_country_id, movie_language, movie_rating, movie_runtime)  # python variables
                           )



            for genre in movie_genres:
                if genre != 'N/A':
                    ############################ MOVIE_GENRE INSERTS  ###############################################
                    # insert movie_genre
                    cursor.execute("""
                        INSERT INTO movie_genre
                            (genre, movie_id)
                        VALUES
                           (%s, %s)
                       ON DUPLICATE KEY UPDATE
                                                         -- no need to update the PK
                           genre  = VALUES(genre),
                           movie_id  = VALUES(movie_id);
                                  """, (genre, movie_id)  # python variables
                                   )





            if len(movie_actors) != 0:
                for x in movie_actors:
                    actor_id = x
                    ############################ MOVIE_ACTOR INSERTS  ###############################################
                    # insert movie_actor data
                    cursor.execute("""
                        INSERT INTO movie_actor
                            (actor_id, movie_id)
                        VALUES
                           (%s, %s)
                       ON DUPLICATE KEY UPDATE
                                                         -- no need to update the PK
                           actor_id  = VALUES(actor_id),
                           movie_id  = VALUES(movie_id);
                                  """, (actor_id, movie_id)  # python variables
                                   )


            if len(movie_directors) != 0:
                for x in movie_directors:
                    director_id = x
                    ############################ MOVIE_DIRECTOR INSERTS  ###############################################
                    # insert movie_director data
                    cursor.execute("""
                        INSERT INTO movie_director
                            (director_id, movie_id)
                        VALUES
                           (%s, %s)
                       ON DUPLICATE KEY UPDATE
                                                         -- no need to update the PK
                           director_id  = VALUES(director_id),
                           movie_id  = VALUES(movie_id);
                                  """, (director_id, movie_id)  # python variables
                                   )




             ####################################### YOUTUBE INSERTS  ###################################

            # insert youtube data
            cursor.execute("""
                INSERT INTO trailers
                    (youtube_id, title, movie_id, view_count, likes)
                VALUES
                    (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                                                  -- no need to update the PK
                    youtube_id  = VALUES(youtube_id),
                    title  = VALUES(title),
                    movie_id  = VALUES(movie_id),
                    view_count  = VALUES(view_count),
                    likes  = VALUES(likes);
                           """, (youtube_id, youtube_title, movie_id, youtube_view_count, youtube_likes)
                           # python variables
                           )

        except:
            print "askdjfhkjasjdflkasdfkl"


        conn.close()
