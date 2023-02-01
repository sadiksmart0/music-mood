import requests
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import neattext as nt
import pandas as pd
import gensim
import en_core_web_md
from database import get_from_all_songs, get_from_recommendations,write_to_recommendations
import spacy
import random


#================================ CLEAN TEXT ============================#
def clean_text(text):
    docx = nt.TextFrame(text)
    song = docx.remove_stopwords().text
    song = docx.remove_puncts().text
    song = docx.remove_special_characters().text

    return song

#================================ PREDICT WITH LYRICS ============================#
def recommend_with_lyrics(text)-> pd.DataFrame:
    song = clean_text(text)
    response = requests.post("http://127.0.0.1:8000/lyrics", json={"text": song})
    response = json.loads(response.text)
    result = query_db(response)
    return result, response


#================================ PREDICT WITH TITLE AND ARTIST ============================#
def recommend_with_title(text)-> pd.DataFrame:
    song = clean_text(text)
    response = requests.post("http://127.0.0.1:8000/title_artist", json={"text": song})
    response = json.loads(response.text)
    result = query_db(response)
    return result, response




tracklist = []
#================================ RECOMMENDED  ===============================#
def final_recommended(df):
    for i in df["dzr_sng_id"][:10].values:
        response = requests.get(f"https://api.deezer.com/track/{i}")
        response = json.loads(response.text)
        tracklist.append(response)
    return tracklist


tracklist = []
#================================ TOP TEN SONGS ===============================#
def top_ten():
    songs = get_from_recommendations()
    for i in songs["dzr_sng_id"][:10].values:
        response = requests.get(f"https://api.deezer.com/track/{i}")
        response = json.loads(response.text)
        tracklist.append(response)
    return tracklist

#============================ VECTORIZE SEARCH PARAMETERS =======================#
nlp = en_core_web_md.load()
sims = []
doc_id = []

def vectorize_search(song_lyrics):
    num = random.randrange(len(song_lyrics))
    song_ref = song_lyrics.iloc[num]
    ref_song = nlp(song_ref["Lyrics"])
    all_songs = [nlp(row) for row in song_lyrics["Lyrics"][:100]]
    return all_songs, ref_song


#============================  GET SIMILAR BASED ON COSINE SIMILARITY =====================#
def get_similar(song_lyrics):
    all_songs, ref_song = vectorize_search(song_lyrics)
    for i in range(len(all_songs)):
        sim = all_songs[i].similarity(ref_song)
        sims.append(sim)
        doc_id.append(i)
        sims_docs = pd.DataFrame(list(zip(doc_id, sims)), columns=["doc_id","sims"])
        sims_docs_sorted = sims_docs.sort_values(by = "sims", ascending=False)
        top = song_lyrics.iloc[sims_docs_sorted["doc_id"][:10]]
        return top


#============================  FETCH FROM   RECOMMEND TABLE   ====================================#
def query_db(mood)-> pd.DataFrame:
    same_mood = get_from_all_songs(mood["mood"])
    return same_mood


#============================  WRITE TO RECOMMEND TABLE     ====================================#
def to_recommend_db(data, mood):
    data.update({"mood": mood["mood"]})
    write_to_recommendations(data)