import streamlit as st
import pandas as pd
import requests
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CineSearch",
    page_icon="🎬",
    layout="wide"
)

# ---------------- UI CSS (SAFE & FIXED) ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* Base font */
html, body {
    font-family: 'Poppins', sans-serif;
}

/* App background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Headings */
h1 {
    font-size: 3rem;
    color: #f5c518;
    text-align: center;
    margin-bottom: 0;
}

h3 {
    text-align: center;
    color: #dddddd;
    margin-top: 5px;
}

/* Movie cards */
.movie-card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 15px;
    padding: 10px;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.movie-card:hover {
    transform: scale(1.08);
    box-shadow: 0px 10px 30px rgba(0,0,0,0.7);
}

.movie-card img {
    border-radius: 12px;
}

.movie-title {
    font-size: 14px;
    font-weight: 600;
    margin-top: 8px;
    color: white;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #f5c518, #ff9900);
    color: black;
    font-weight: bold;
    border-radius: 30px;
    padding: 12px 25px;
    border: none;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #ff9900, #f5c518);
}

/* Selectbox label */
label {
    color: white !important;
    font-weight: 600;
}

/* Selected value text */
div[data-baseweb="select"] > div {
    color: black !important;
}

/* Dropdown options */
div[data-baseweb="popover"] {
    color: black !important;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    background-color: white !important;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
}

div[data-testid="stChatMessage"] p {
    color: black !important;
}

/* Chat input */
div[data-testid="stChatInput"] textarea {
    color: black !important;
    background-color: white !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #555 !important;
}

div[data-testid="stChatInput"] label {
    color: black !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
with open("movie_data.pkl", "rb") as file:
    movies, cosine_sim = pickle.load(file)

# ---------------- RECOMMENDATION FUNCTION ----------------
def get_recommendations(title):
    idx = movies[movies["title"] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies[["title", "movie_id"]].iloc[movie_indices]

# ---------------- POSTER FETCH ----------------
def fetch_poster(movie_id):
    api_key = "7b995d3c6fd91a2284b4ad8cb390c7b8"  # TMDB API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

# ---------------- HEADER ----------------
st.markdown("<h1>🎬 CineSearch</h1>", unsafe_allow_html=True)
st.markdown("<h3>AI-Powered Movie Recommendation Engine 🍿</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------------- MOVIE SELECT ----------------
selected_movie = st.selectbox(
    "🎥 Choose a movie you like",
    movies["title"].values
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- BUTTON ACTION ----------------
if st.button("🍿 Recommend Movies"):
    recommendations = get_recommendations(selected_movie)

    st.markdown("<h3>⭐ Top 10 Movies You’ll Love</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i + 5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]["title"]
                movie_id = recommendations.iloc[j]["movie_id"]
                poster_url = fetch_poster(movie_id)

                with col:
                    st.markdown(f"""
                        <div class="movie-card">
                            <img src="{poster_url}" width="160"/>
                            <div class="movie-title">{movie_title}</div>
                        </div>
                    """, unsafe_allow_html=True)
