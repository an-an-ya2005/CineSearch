import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading dataset...")

# ✅ Use the file you ACTUALLY have
movies = pd.read_csv("tmdb_5000_movies.csv")

# Keep only required columns
movies = movies[['title', 'id', 'overview']]
movies.dropna(inplace=True)

# Rename for app compatibility
movies.rename(columns={'id': 'movie_id'}, inplace=True)

# 🔽 VERY IMPORTANT: reduce size
movies = movies.head(3000)

print(f"Movies used: {len(movies)}")

# Vectorization
cv = CountVectorizer(stop_words='english', max_features=5000)
vectors = cv.fit_transform(movies['overview']).toarray()

print("Calculating cosine similarity...")
cosine_sim = cosine_similarity(vectors)

# Save pickle
with open("movie_data.pkl", "wb") as f:
    pickle.dump((movies[['title', 'movie_id']], cosine_sim), f)

print("✅ movie_data.pkl created successfully")
