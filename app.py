import streamlit as st
import pandas as pd
import numpy as np
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CineSearch",
    page_icon="🎬",
    layout="wide"
)

# ---------------- UI CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

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

.stButton > button {
    background: linear-gradient(90deg, #f5c518, #ff9900);
    color: black;
    font-weight: bold;
    border-radius: 30px;
    padding: 12px 25px;
    border: none;
}

label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA (DEPLOYMENT SAFE) ----------------
@st.cache_data
def load_data():
    movies = pd.read_csv("movies.csv")
    cosine_sim = np.load("cosine_sim.npy")
    return movies, cosine_sim

movies, cosine_sim = load_data()

# ---------------- RECOMMENDATION FUNCTION ----------------
def get_recommendations(title):
    idx = movies[movies["title"] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices]

# ---------------- POSTER FETCH ----------------
def fetch_poster(movie_id):
    api_key = "7b995d3c6fd91a2284b4ad8cb390c7b8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data = requests.get(url).json()
    if data.get("poster_path"):
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    return ""

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
