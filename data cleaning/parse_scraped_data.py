import os
import re
import csv
import json
import locale
import collections


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def parse_facebook_likes_number(num_likes_string):
    if not num_likes_string:
        return 0
    size = len(num_likes_string)
    if num_likes_string[-1] == 'K':
        return int(float(num_likes_string[ : size - 1]) * 1000)
    elif num_likes_string.isdigit():
        return int(num_likes_string)
    elif num_likes_string == 'One':
        return 1
    else:
        return 0

def parse_price(price):
    if not price:
        return 0
    elif price[0] == '$':
        return locale.atoi(re.sub('[^0-9,]', "", price))
    elif price[0] == '€':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 1.06
    elif price[0] == '£':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 1.26
    elif price[0:3] == 'CAD':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.76
    elif price[0:3] == 'CNY':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.14
    elif price[0:3] == 'AUD':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.75
    elif price[0:3] == 'INR':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.015
    elif price[0:3] == 'THB':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.028
    elif price[0:3] == 'KRW':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.00085
    elif price[0:3] == 'HKD':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.13
    elif price[0:3] == 'BRL':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.3
    elif price[0:3] == 'JPY':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.0086
    elif price[0:3] == 'SEK':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.0086
    elif price[0:3] == 'ZAR':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.072
    elif price[0:3] == 'NZD':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.72
    elif price[0:3] == 'NOK':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.12
    elif price[0:3] == 'CHF':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.98
    elif price[0:3] == 'CZK':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.98
    elif price[0:3] == 'DKK':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.14
    elif price[0:3] == 'HUF':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.0034
    elif price[0:3] == 'RUR':
        return locale.atoi(re.sub('[^0-9,]', "", price)) * 0.016
    else:
        return 0

def parse_duration(duration_string):
    if not duration_string:
        return 0
    #n = re.findall('[0-9,]+', duration_string)
    if "min" in duration_string:
        if "h" in duration_string: # eg: "2h 49min"
            s = duration_string.split("h")
            hours = int(s[0])
            if len(s) > 1: # has minute number
                if "min" in s[1]:
                    minutes = int(s[1].strip().split("min")[0])
                else:
                    minutes = 0
            else:
                minutes = 0
            return 60 * hours + minutes
        else: # eg: "169 min"
            return int(duration_string.split('min')[0])
    else:
        if "h" in duration_string: # eg: "2h"
            return int(duration_string.split('h')[0].strip()) * 60
        else:
            return None

def remove_non_ascii_chars_in_string(s):
    # eg: u'Avatar\xa0' ---> u'Avatar'
    return re.sub(r'[^\x00-\x7F]+','', s) 

def load_unparsed_movie_metadata():
    try:
        with open(os.path.join("/Users/songjiang/movie_rating_prediction/imdb_output.json"), "r") as f:
            movies = json.load(f)
            return movies
    except:
        print("Cannot load the unparsed movie metadata file!")
        return None



def parse_one_movie_metadata(movie):
    if not movie:
        return None

    parsed_movie = {}

    # parsed_movie['movie_imdb_link'] = movie['movie_imdb_link']
    # parsed_movie['movie_title'] = movie['movie_title'].encode('utf-8')
    # parsed_movie['num_voted_users'] = movie['num_voted_users']
    # parsed_movie['num_user_for_reviews'] = movie['num_user_for_reviews']
    # parsed_movie['gross'] = 0 if movie['gross'] is None or len(movie['gross']) == 0 else parse_price(movie['gross'][0].strip())
    parsed_movie['budget'] = 0 if movie['budget'] is None or len(movie['budget']) == 0 else parse_price(movie['budget'][0].strip())
    parsed_movie['movie_fb_likes'] = parse_facebook_likes_number(movie['num_facebook_like'])
    parsed_movie['imdb_score'] = float(movie['imdb_score'][0].strip())
    # parsed_movie['num_critic_for_reviews'] = 0 if movie['num_critic_for_reviews'] is None else movie['num_critic_for_reviews']

    # parse movie duration
    duration = movie['duration']
    if not duration:
        parsed_movie['duration'] = 0
    else:
        if len(duration) == 1:
            parsed_movie['duration'] = parse_duration(duration[0].strip())
        else:
            parsed_movie['duration'] = parse_duration(duration[-1].strip())

    # get cast's total facebook likes (all actors and actress listed in movie's main page)
    cast_info = movie['cast_info']
    cast_total_facebook_likes = 0
    for actor in cast_info:
        _num = actor['actor_facebook_likes']
        if not _num:
            continue
        num = parse_facebook_likes_number(_num)
        cast_total_facebook_likes += num
    parsed_movie['cast_total_fb_likes'] = cast_total_facebook_likes

    # get top 4 main actors/actress' name and fb likes
    cast_size = len(cast_info)
    main_actor_index = []
    if cast_size % 2 == 0:
        main_actor_index.append(0)
        main_actor_index.append(int(cast_size/2))
        main_actor_index.append(1)
        main_actor_index.append(int(cast_size/2+1))
    else:
        main_actor_index.append(0)
        main_actor_index.append(int((cast_size+1) / 2))
        main_actor_index.append(1)
        main_actor_index.append(int((cast_size+1) / 2 + 1))

    for k in range(len(main_actor_index)):
        # _key_of_actor_name = "actor_{}_name".format(k + 1)
        _key_of_facebook_likes = "actor{}_fb_likes".format(k + 1)
        if k < cast_size:
            # parsed_movie[_key_of_actor_name] = cast_info[main_actor_index[k]]['actor_name'].encode('utf-8')
            parsed_movie[_key_of_facebook_likes] = parse_facebook_likes_number(cast_info[main_actor_index[k]]['actor_facebook_likes'])
        else:
            # parsed_movie[_key_of_actor_name] = None
            parsed_movie[_key_of_facebook_likes] = 0


    # parse director info
    director_info = movie['director_info']
    if not director_info:
        # parsed_movie['director_name'] = None
        parsed_movie['director_fb_likes'] = 0
    else:
        # parsed_movie['director_name'] = director_info['director_name'].encode('utf-8')
        parsed_movie['director_fb_likes'] = parse_facebook_likes_number(director_info['director_facebook_likes'])
    return parsed_movie


def parse_all_movies():
    movies = load_unparsed_movie_metadata()
    with open("movie_metadata_final.csv", "w") as f:
        header_was_written = False
        for i, movie in enumerate(movies):
            parsed_movie = parse_one_movie_metadata(movie)
            if parsed_movie['actor1_fb_likes'] < 200 or parsed_movie['actor2_fb_likes'] < 100 or \
               parsed_movie['actor3_fb_likes'] <20 or parsed_movie['actor4_fb_likes'] <10 or \
               parsed_movie['director_fb_likes'] < 30 or parsed_movie['movie_fb_likes'] == 0 or \
               parsed_movie['budget'] < 100000 or parsed_movie['duration'] < 60:
                continue
            w = csv.DictWriter(f, parsed_movie.keys())
            if not header_was_written:
                w.writeheader()
                header_was_written = True
            w.writerow(parsed_movie)

parse_all_movies()