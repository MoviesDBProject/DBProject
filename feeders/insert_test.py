# Server Connection to MySQL:

import MySQLdb
from dbpedia_feeder import *
from pycountry import *

# conn = MySQLdb.connect(host= "localhost",
#                  user="root",
#                  passwd="",
#                  db="dbproject")
# cursor = conn.cursor()





countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha2


def actors_insert(actors_table):
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="",
                           db="dbproject")

    cursor = conn.cursor()

    for actor in actors_table:
        try:
            actor_id = actor[ID]
            actor_name = actor[NAME]
            actor_date_of_birth = actor[BIRTH_DATE]
            actor_birth_place = actor[BIRTH_PLACE].rsplit(',', 1)[1].lstrip()
            actor_birth_place_id = countries[actor_birth_place]

            ############################ COUNTRY INSERTS  ###############################################
            # insert actor country
            cursor.execute("""
                INSERT INTO country
                    (country_id, country)
                VALUES
                   (%s, %s)
               ON DUPLICATE KEY UPDATE
                                                 -- no need to update the PK
                   country_id  = VALUES(country_id),
                   country   = VALUES(country) ;
                          """, (actor_birth_place_id, actor_birth_place)  # python variables
                           )


            ############################ ACTOR INSERTS  ###############################################
            # insert actor data
            cursor.execute("""
                INSERT INTO actors
                    (actor_id, name, date_of_birth, birth_place_id)
                VALUES
                   (%s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE
                                                 -- no need to update the PK
                   actor_id  = VALUES(actor_id),
                   name   = VALUES(name),
                   date_of_birth  = VALUES(date_of_birth),
                   birth_place_id  = VALUES(birth_place_id);
                          """, (actor_id, actor_name, actor_date_of_birth, actor_birth_place_id)  # python variables
                           )

        except:
            print "askdjfhkjasjdflkasdfkl"

        conn.close()





def directors_insert(directors_table):
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="",
                           db="dbproject")

    cursor = conn.cursor()

    for director in directors_table:
        try:
            director_id = director[ID]
            director_name = director[NAME]
            director_date_of_birth = director[BIRTH_DATE]
            director_birth_place = director[BIRTH_PLACE].rsplit(',', 1)[1].lstrip()
            director_birth_place_id = countries[director_birth_place]

            ############################ COUNTRY INSERTS  ###############################################
            # insert director country
            cursor.execute("""
                INSERT INTO country
                    (country_id, country)
                VALUES
                   (%s, %s)
               ON DUPLICATE KEY UPDATE
                                                 -- no need to update the PK
                   country_id  = VALUES(country_id),
                   country   = VALUES(country) ;
                          """, (director_birth_place_id, director_birth_place)  # python variables
                           )


            ############################ DIRECTOR INSERTS  ###############################################
            # insert director data
            cursor.execute("""
                INSERT INTO directors
                    (director_id, name, date_of_birth, birth_place_id)
                VALUES
                   (%s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE
                                                 -- no need to update the PK
                   director_id  = VALUES(director_id),
                   name   = VALUES(name),
                   date_of_birth  = VALUES(date_of_birth),
                   birth_place_id  = VALUES(birth_place_id);
                          """, (director_id, director_name, director_date_of_birth, director_birth_place_id)  # python variables
                           )

        except:
            print "askdjfhkjasjdflkasdfkl"

        conn.close()






def movies_insert(movies_table):
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="",
                           db="dbproject")

    cursor = conn.cursor()

    for movie in movies_table:
        try:

            movie_actors = movie[ACTORS]
            movie_directors = movie[DIRECTORS]

            movie_id = movie[ID]
            movie_name = movie[NAME]
            if len(movie[COUNTRY]) != 0:
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
                    (movie_id, title, country_id)
                VALUES
                   (%s, %s, %s)
               ON DUPLICATE KEY UPDATE
                                                 -- no need to update the PK
                   movie_id  = VALUES(movie_id),
                   title   = VALUES(title),,
                   country_id  = VALUES(country_id);
                          """, (movie_id, movie_name, movie_country_id)  # python variables
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





        except:
            print "askdjfhkjasjdflkasdfkl"


        conn.close()




data_dict = {}

# data_dict['country_data'] = {}
# data_dict['language_data'] = {}
data_dict['movie_data'] = {}
data_dict['actors_data'] = []  # list of actors, not a dictionary
data_dict['youtube_data'] = {}
data_dict['director'] = {}


def test_insert():
    try:
        result = get_movies_from_dbpedia()
        print result
        # default_date = '1800-01-01'

        data_dict['movie_data']['movie_id'] = result[0]['movie_id']
        data_dict['movie_data']['title'] = result[0]['title']
        data_dict['movie_data']['country'] = result[0]['country']
        data_dict['movie_data']['country_id'] = countries[result[0]['country']]
        data_dict['movie_data']['language'] = result[0]['language']
        # get language hash
        # data_dict['movie_data']['language_id'] = language hash
        # maybe do some default value if year does not exist?
        data_dict['movie_data']['year'] = result[0]['year']
        data_dict['movie_data']['description'] = result[0]['abstract']

        # youtube data
        youtube_result = result[0]['youtube']
        data_dict['youtube_data']['youtube_id'] = youtube_result['youtube_id']
        data_dict['youtube_data']['youtube_title'] = youtube_result['title']
        data_dict['youtube_data']['youtube_view_count'] = youtube_result['view_count']
        data_dict['youtube_data']['youtube_likes'] = youtube_result['likes']

        # actors data
        actors_dict = result['actors']
        single_actor = {}
        for actor in actors_dict:
            single_actor['actor_id'] = actor['actor_id']
            single_actor['name'] = actor['name']

            if 'date_of_birth' in actor:
                single_actor['date_of_birth'] = actor['date_of_birth']
            else:
                single_actor['date_of_birth'] = ''

            if 'birth_place' in actor:
                actor_country = actor['date_of_birth'].rsplit(',', 1)[1].lstrip()
                if actor_country == 'Kingdom of Egypt':
                    actor_country = 'Egypt'

                single_actor['birth_place'] = actor_country
                single_actor['birth_place_id'] = countries[actor_country]
            else:
                single_actor['birth_place'] = ''

            data_dict['actors_data'].append(single_actor)

        # director data
        data_dict['director_data']['director_id'] = result[0]['director']['director_id']
        data_dict['director_data']['name'] = result[0]['director']['name']
        data_dict['director_data']['date_of_birth'] = result[0]['director']['date_of_birth']
        director_country = result[0]['director']['date_of_birth'].rsplit(',', 1)[1].lstrip()
        data_dict['director_data']['birth_place'] = director_country
        data_dict['director_data']['birth_place_id'] = countries[director_country]


        # # movie specific data
        # movie_title = result[0]['title']
        # movie_id = 1
        #
        # if 'language' in result[0]:
        #     movie_language = result[0]['language']
        #     movie_language_id = 1
        # else:
        #     movie_language = ""
        #
        # if 'country' in result[0]:
        #     movie_country = result[0]['country']
        #     movie_country_id = countries[movie_country]
        # else:
        #     movie_country_id = ""
        #
        # if 'abstract' in result[0]:
        #     movie_description = result[0]['abstract']
        # else:
        #     movie_description = ""
        #
        #
        # # youtube data
        # if 'youtube' in result[0]:
        #     youtube_result = result[0]['youtube']
        #
        #     youtube_id = youtube_result['youtube_id']
        #     youtube_title = youtube_result['title']
        #     youtube_view_count = youtube_result['view_count']
        #     youtube_likes = youtube_result['likes']
        #
        #     youtube_movie_id = movie_id
        #
        # else:
        #     youtube_result = "" # do not add a youtube entry
        #
        #
        #
        # # actors data
        # if 'actors' in result:
        #     actors_dict = result['actors']
        #     single_actor = {}
        #     for actor in actors_dict:
        #         single_actor['name'] = actor['name']
        #
        #         if 'date_of_birth' in actor:
        #             single_actor['date_of_birth'] = actor['date_of_birth']
        #         else:
        #             single_actor['date_of_birth'] = ''
        #
        #         if 'birth_place' in actor:
        #             actor_country = actor['date_of_birth'].rsplit(',', 1)[1].lstrip()
        #             if actor_country == 'Kingdom of Egypt':
        #                 actor_country = 'Egypt'
        #
        #             single_actor['birth_place'] = countries[actor_country]
        #         else:
        #             single_actor['birth_place'] = ''
        #
        #         actors_data.append(single_actor)
        #
        #
        #
        # # director data
        # if 'director' in result[0]:
        #     director_name = result[0]['director']['name']
        #
        #     if 'birth_date' in result[0]['director']:
        #         director_date_of_birth = result[0]['director']['birth_date']
        #     else:
        #         director_date_of_birth = ''
        #
        #     if 'birth_place' in result[0]['director']:
        #         director_country = result[0]['director']['date_of_birth'].rsplit(',', 1)[1].lstrip()
        #         if director_country == 'Kingdom of Egypt':
        #             director_country = 'Egypt'
        #
        #         director_country_id = countries[director_country]
        #     else:
        #         director_country_id = ''


    except:
        print "ERROR!!!!!!!!!!!!!!!!!!!!"


def update_tables(data):
    movie_country_id = data_dict['movie_data']['country_id']
    movie_country = data_dict['movie_data']['country']
    movie_language_id = data_dict['movie_data']['language_id']
    movie_language = data_dict['movie_data']['language']
    movie_id = data_dict['movie_data']['movie_id']
    movie_title = data_dict['movie_data']['title']
    movie_description = data_dict['movie_data']['description']
    movie_year = data_dict['movie_data']['year']

    youtube_id = data_dict['youtube_data']['youtube_id']
    youtube_title = data_dict['youtube_data']['youtube_title']
    youtube_view_count = data_dict['youtube_data']['youtube_view_count']
    youtube_likes = data_dict['youtube_data']['youtube_likes']

    director_id = data_dict['director_data']['director_id']
    director_name = data_dict['director_data']['name']
    director_date_of_birth = data_dict['director_data']['date_of_birth']
    director_country = data_dict['director_data']['birth_place']
    director_country_id = data_dict['director_data']['birth_place_id']

    actor_country = []
    actor_country_id = []
    actor_id = []
    actor_name = []
    actor_date_of_birth = []
    for actor in data_dict['actor_data']:
        actor_country.append(actor['birth_place'])
        actor_country_id.append(actor['birth_place_id'])
        actor_id.append(actor['actor_id'])
        actor_name.append(actor['name'])
        actor_date_of_birth.append(actor['date_of_birth'])

    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="",
                           db="dbproject")

    cursor = conn.cursor()

    try:
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

        # insert director country
        cursor.execute("""
           INSERT INTO country
               (country_id, name)
           VALUES
               (%s, %s)
           ON DUPLICATE KEY UPDATE
                                             -- no need to update the PK
               country_id  = VALUES(country_id),
               name   = VALUES(name) ;
                      """, (director_country_id, director_country)  # python variables
                       )

        # insert actors country
        for i in range(len(actor_country)):
            cursor.execute("""
               INSERT INTO country
                   (country_id, name)
               VALUES
                   (%s, %s)
               ON DUPLICATE KEY UPDATE
                                                 -- no need to update the PK
                   country_id  = VALUES(country_id),
                   name   = VALUES(name) ;
                          """, (actor_country_id[i], actor_country[i])  # python variables
                           )

        ####################################### LANGUAGE INSERTS  ###################################

        # insert movie language
        cursor.execute("""
           INSERT INTO language
               (language_id, language)
           VALUES
               (%s, %s)
           ON DUPLICATE KEY UPDATE
                                             -- no need to update the PK
               language_id  = VALUES(language_id),
               language   = VALUES(language) ;
                      """, (movie_language_id, movie_language)  # python variables
                       )

        ####################################### MOVIE INSERTS  ###################################

        # insert movie data
        cursor.execute("""
           INSERT INTO movies
               (movie_id, title, year, language_id, country_id, description)
           VALUES
               (%s, %s, %s, %s, %s, %s)
           ON DUPLICATE KEY UPDATE
                                             -- no need to update the PK
               movie_id  = VALUES(movie_id),
               title  = VALUES(title),
               year  = VALUES(year),
               language_id  = VALUES(language_id),
               country_id  = VALUES(country_id),
               description  = VALUES(description);
                      """, (movie_id, movie_title, movie_year, movie_language_id, movie_country_id, movie_description)
                       # python variables
                       )

        ####################################### YOUTUBE INSERTS  ###################################

        # insert youtube data
        cursor.execute("""
           INSERT INTO movies
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
                      """, (youtube_id, youtube_title, movie_id, youtube_view_count, youtube_likes)  # python variables
                       )


        #    # first insert the language and country of the movie
        #    cursor.execute("""INSERT INTO country VALUES (%s,%s)""", (movie_country_id, movie_country))
        #    cursor.execute("""INSERT INTO language VALUES (%s,%s)""", (movie_language_id, movie_language))
        #
        #     # second insert movie data
        #    cursor.execute("""INSERT INTO movies VALUES (%s,%s,%s,%s,%s,%s,%s)""", (1, movie_title,1900,movie_language_id,movie_country_id,100,movie_description))
        #
        #    conn.commit()
        #    print "asdkjfkjasdfjadskfl"
        #    cursor.execute("""SELECT * FROM movies)""")
        # except Exception as e:
        #    print str(e)
        #    print "FAILEDDDDD"
        #    conn.rollback()
        #
        #
        # conn.close()

    except:
        print "asdfkasdf"


if __name__ == '__main__':
    # test_insert()

    conn = MySQLdb.connect(host="localhost",
                           port=3306,
                           user="root",
                           passwd="",
                           db="dbproject")

    cursor = conn.cursor()

    try:
        cursor.execute("""INSERT INTO country VALUES (%s,%s)""", (10, "test country"))
        # cursor.execute("SELECT VERSION()")
        cursor.execute("""SELECT * FROM country WHERE country.country_id = 10""")
        row = cursor.fetchone()
        print row
    except Exception as e:
        print e


    conn.close()
