from imports import *
from scipy import spatial
<<<<<<< HEAD
from streamlit.connections import SQLConnection
import streamlit as st
from sqlalchemy import text
import traceback
import logging
=======
>>>>>>> parent of f13de00 (hopefully the deployment works)

conn = sqlite3.connect('movie_main.db', check_same_thread=False)

c = conn.cursor()

import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def clean_text(text): 
    if(text == None):
        return []
    return [word.lower().replace(" ", "") for word in text.split(",")]

def clean_plot(text):
    if(text == None):
        return []
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens]
    tokens = [words for words in tokens if words.isalpha()]
    tokens = [words for words in tokens if not words in stop_words]
    tokens = [stemmer.stem(words) for words in tokens]
    return tokens

def clean_df(df):

    df['genre'] = df['genre'].apply(clean_text)
    df['cast'] = df['cast'].apply(clean_text)
    df['director'] = df['director'].apply(clean_text)  
    df['plot'] = df['plot'].apply(clean_plot)

def to_string(list):
    if(list == None):
        return ""
    return ' '.join(list)

def get_film_vector(idx, ser, model):
    vector = np.zeros(100)
    word_list = ser.iloc[idx].split()
    for words in word_list:
        vector += model.wv.get_vector(words)

    return vector

def get_rex(movie_name, dir_w, cast_w, gen_w):

    init_resp = requests.get(f"http://www.omdbapi.com/?apikey=508132df&t={movie_name}")

    resp_dict = json.loads(init_resp.text)

    if(resp_dict["Response"] == "True"):
<<<<<<< HEAD
        list = conn.query(f"select * from movies where title = \"{resp_dict['Title']}\"")
        print(list)
        if(len(list.index) == 0):
            try:
                with conn.session as s:
                    s.execute(text("insert into movies values (:title, :genre, :director, :cast, :plot)"), params = {'title': resp_dict["Title"], 'genre': resp_dict["Genre"], 'director': resp_dict["Director"], 'cast' : resp_dict["Actors"], 'plot' : resp_dict["Plot"]})
                    s.commit()
            except Exception as e:
                logging.error(traceback.format_exc())
=======
        movie_title = resp_dict["Title"]
        c.execute(f"SELECT * FROM movies where title = \"{movie_title}\"")
        list = c.fetchone()
        if(list == None):
            newmovie = True
            with conn:
                c.execute("INSERT INTO movies VALUES (:title, :genre, :director, :cast, :plot)", {'title': resp_dict["Title"], 'genre': resp_dict["Genre"], 'director': resp_dict["Director"], 'cast' : resp_dict["Actors"], 'plot' : resp_dict["Plot"]})
                conn.commit()
>>>>>>> parent of f13de00 (hopefully the deployment works)
    else:
        return 0, ["Movie Not Found"]
    
    sql_query = pd.read_sql_query("select * from movies", conn)

    movie_dataframe = pd.DataFrame(sql_query)

    clean_df(movie_dataframe)

    Ser = gen_w * movie_dataframe['genre'] + cast_w*movie_dataframe['cast'] + dir_w*movie_dataframe['director'] + movie_dataframe['plot']
    Ser = Ser.apply(to_string)

    indices = pd.Series(movie_dataframe.index, index=movie_dataframe['title']).drop_duplicates()

    data = []
    for summs in Ser.values:
        list = summs.split()
        data.append(list)
        
    vec_model = Word2Vec(data, window=10, min_count=1, workers=4, sg = 1)
    
    idx = indices[resp_dict["Title"]]
    the_vec = get_film_vector(idx, Ser, vec_model)
    sims = []
    for i in range(len(Ser)):
        vec2 = get_film_vector(i, Ser, vec_model)
        cossim = 1 - spatial.distance.cosine(the_vec, vec2)
        sims.append((cossim, i))

    sims = sorted(sims)
    recclist = []
    for _, ind in sims[-11:-1]:
        recclist.append(movie_dataframe['title'].values[ind])

    recclist.reverse()

    return 1, recclist



    


    

    


    


