import streamlit as st
from PIL import Image
from predict import recommend_with_lyrics, recommend_with_title, top_ten, get_similar, final_recommended,to_recommend_db
import base64
import uuid
import datetime

#================ Gif loader ===================#
file_ = open("C:/Users/A.M. MUKTAR/Desktop/ACTION LEARNING/Music_app/images/prof.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

#================ Side Bar ===================#
add_selectbox = st.sidebar.selectbox(
    "Explore our top 10",
    ("Happy", "Sad", "Angry","Relaxed")
)




#================ App Header ===================#
head, photo = st.columns(2)    
with head:   
    st.title("With music there is no tension.")

with photo:
    st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">', unsafe_allow_html=True,)



#========================   RECOMMMENDATION VIEW  ==================================#
def view(result):
    img_col, play_col = st.columns(2)
    for song in result:
        with img_col:
            st.subheader(song["title"])
            st.write(song["artist"]["name"])
            st.image(song["artist"]["picture"])
        with play_col:
            st.subheader(song["album"]["title"])
            st.write(f'Duration: {round(song["duration"]/60,2)} min')
            st.markdown(f"[![Foo](https://cdn-icons-png.flaticon.com/128/9458/9458362.png)]({song['link']})")



#================ App tabs ===================#
tab1, tab2,tab3 = st.tabs(["Lyrics","Artist and Song Title","Top 10"])

#================  BY LYRICS ===================#
with tab1:
    st.subheader("Search by Lyrics")
    txt = st.text_area('Insert Song Lyrics', '''
    It was the best of times, it was the worst of times, it was
    the age of wisdom, it was the age of foolishness, it was
    the epoch of belief, it was the epoch of incredulity, it
    was the season of Light, it was the season of Darkness, it
    was the spring of hope, it was the winter of despair, (...)
    ''')
    if st.button('Submit'):
        result, mood = recommend_with_lyrics(txt)
        rec_songs = get_similar(result)
        result = final_recommended(rec_songs)
        view(result)
        #st.write(rec_songs)

#================ By ARTIST AND SONG TITLE  ===================#
with tab2:
    st.subheader("Get Your artist and song")
    artist = st.text_input("Enter Artist Name", placeholder="Eminem", help="Must not be blank")
    title = st.text_input("Enter Song Title",placeholder="Not Afraid", help="Must not be blank")

    # String of User Input
    data = title+" "+artist
    song_data = {
        'artist': artist,
        'title': title,
        'recommendation_id': str(uuid.uuid1()),
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if st.button('Get Recommendation'):
        result1, mood  = recommend_with_title(data)
        to_recommend_db(song_data, mood)
        recommended_song = get_similar(result1)
        result = final_recommended(recommended_song)
        view(result)
        #st.write(recommended_song)

#========================== GET TOP TEN =========================#
with tab3:
    st.subheader("Top 10")
    result3 = top_ten()
    view(result3)

