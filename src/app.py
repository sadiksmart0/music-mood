import streamlit as st
from PIL import Image
from predict import predict, top_ten
import base64


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
        result = predict(txt)
        st.write(result)

#================ By ARTIST AND SONG TITLE  ===================#
with tab2:
    st.subheader("Get Your artist and song")
    artist = st.text_input("Enter Artist Name", placeholder="Eminem", help="Must not be blank")
    title = st.text_input("Enter Song Title",placeholder="Not Afraid", help="Must not be blank")
    if st.button('Get Recommendation'):
        result1 = predict(artist+" "+title)
        st.write(result1)

#========================== GET TOP TEN =========================#
with tab3:
    st.subheader("Top 10")
    result3 = top_ten()
    img_col, play_col = st.columns(2)
    for song in result3:
        with img_col:
            st.subheader(song["title"])
            st.write(song["artist"]["name"])
            st.image(song["artist"]["picture"])
        with play_col:
            st.subheader(song["album"]["title"])
            st.write(f'Duration: {round(song["duration"]/60,2)} min')
            st.markdown(f"[![Foo](https://cdn-icons-png.flaticon.com/128/9458/9458362.png)]({song['link']})")
        




