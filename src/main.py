#=============================   Import Dependencies  =========================================#
from fastapi import FastAPI
import pandas as pd
import uvicorn
from pydantic import BaseModel, validator
import numpy as np
from io import BytesIO
import datetime

from database import write_to_all_songs

#================================= Validating File  ============================================#
class Data(BaseModel):
    text: str

#================================= Declaring FASTAPI  ============================================#
# FastApi declaration
app = FastAPI(title='Emotional Recommender', version='1.0',
              description='BERT Models are used to predict the emotion from song lyrics')




#================================= File Prediction ==========================================+#

@app.post("/lyrics")
def user_lyrics(lyrics: Data):
    return {"mood": "Relaxed"}


@app.post("/title_artist")
def user_artist_title(title_artist: Data):
    return {"mood": "Angry"}




if __name__ == '__main__':
    songs = pd.read_csv("C:/Users/A.M. MUKTAR/music-mood-recognition/dataset/lyrics_1.csv")
    write_to_all_songs(songs)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
