import pandas as pd
import streamlit as st
import requests
import pickle  # Added missing import

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    default_image = "https://via.placeholder.com/500x750?text=Poster+Not+Found"  # default URL
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0ee09ad9eb01e3c05a907ffbe7e44dba&language=en-US'
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else default_image
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return default_image

# Function to recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set page configuration
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    /* General styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Title styling */
    h1 {
        text-align: center;
        font-size: 3rem;
        color: #e94560;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }
    
    /* Selectbox styling */
    .stSelectbox {
        background-color: #2a2a4e;
        border-radius: 10px;
        padding: 10px;
    }
    .stSelectbox > div > div > div {
        color: #ffffff !important;
        font-size: 1.2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #e94560;
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        border: none;
        transition: all 0.3s ease;
        display: block;
        margin: 1.5rem auto;
    }
    .stButton > button:hover {
        background-color: #ff6b6b;
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
    }
    
    /* Movie card styling */
    .movie-card {
        background-color: #2a2a4e;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(233, 69, 96, 0.3);
    }
    
    .movie-card img {
        border-radius: 10px;
        width: 100%;
        height: auto;
        max-height: 300px;
        object-fit: cover;
    }
    
    .movie-title {
        font-size: 1.1rem;
        color: #ffffff;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }
        .movie-card {
            margin: 0.5rem 0;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Add custom font
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Page title
st.title("Movie Recommender System")

# Movie selection
selected_movie_name = st.selectbox(
    'Select a Movie',
    movies['title'].values,
    help="Choose a movie to get recommendations"
)

# Recommend button
if st.button('Get Recommendations'):
    names, posters = recommend(selected_movie_name)
    
    # Display recommendations in a grid
    st.markdown("<h2 style='text-align: center; color: #ffffff;'>Recommended Movies</h2>", unsafe_allow_html=True)
    cols = st.columns(5 if len(names) >= 5 else len(names))
    
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f"""
                <div class='movie-card'>
                    <img src='{poster}' alt='{name}'>
                    <div class='movie-title'>{name}</div>
                </div>
            """, unsafe_allow_html=True)

# Add a footer
st.markdown("""
    <div style='text-align: center; color: #aaaaaa; margin-top: 2rem;'>
        Powered by The Movie Database (TMDB) API
    </div>
""", unsafe_allow_html=True)