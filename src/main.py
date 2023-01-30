#=============================   Import Dependencies  =========================================#
from fastapi import FastAPI
import pandas as pd
import uvicorn
from pydantic import BaseModel, validator
import numpy as np
from io import BytesIO
import datetime


class Data(BaseModel):
    text: str



# FastApi declaration
app = FastAPI(title='Emotional Recommender', version='1.0',
              description='Model Serving point')


@app.post("/text")
def user_predict(text: Data):
    return text


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
