import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading dataset...")
movies = pd.read_csv("tmdb_5000_movies.csv")

# Keep required columns
movies = movies[['id', 'title', 'overview']].dropna()
movies = movies.sample(2000, random_state=42).reset_index(drop=True)

print("Vectorizing text...")
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
vectors = tfidf.fit_transform(movies['overview'])

print("Calculating cosine similarity...")
cosine_sim = cosine_similarity(vectors).astype(np.float32)

# Save movies
movies = movies[['id', 'title']]
movies.columns = ['movie_id', 'title']
movies.to_csv("movies.csv", index=False)

# Save similarity matrix
np.save("cosine_sim.npy", cosine_sim)

print("✅ movies.csv & cosine_sim.npy created")
print("🚀 Ready for deployment")
