import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import neattext as nt
import requests
import pandas as pd


# import tensorflow_hub as hub
#import tensorflow as tf
#import tensorflow_text



#================================ CLEAN TEXT ============================#
def clean_text(text):
    docx = nt.TextFrame(text)
    song = docx.remove_stopwords().text
    song = docx.remove_puncts().text
    song = docx.remove_special_characters().text

    return song

#================================ PREDICT MODEL ============================#
def predict(text):
    song = clean_text(text)
    response = requests.post("http://127.0.0.1:8000/text", json={"text": song})
    return response.text


tracklist = []

#================================ TOP TEN SONGS ===============================#
def top_ten():
    songs = pd.read_csv("C:/Users/A.M. MUKTAR/Desktop/ACTION LEARNING/Music_app/dataset/lyrics.csv")
    for i in songs["dzr_sng_id"][:10].values:
        response = requests.get(f"https://api.deezer.com/track/{i}")
        response = json.loads(response.text)
        tracklist.append(response)
    return tracklist

