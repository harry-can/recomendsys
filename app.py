import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
   response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3b740953eb7873acf6c06a908ff79449&language=en-US'.format(movie_id))
   data = response.json()
   print(data)
   return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]

    recommended_movies = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append({
            'name': movies.iloc[i[0]].title,
            'poster': fetch_poster(movie_id)
        })

    return recommended_movies
movies_dic = pickle.load(open('movie_name.pkl','rb'))
movies = pd.DataFrame(movies_dic)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Recommendation System')

option = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)
if st.button('Recommend'):
    recommendations = recommend(option)
    num_cols = 4  # Number of columns in the grid layout
    num_recommendations = len(recommendations)

    # Calculate the number of rows needed based on the number of recommendations and columns
    num_rows = (num_recommendations - 1) // num_cols + 1

    # Create the grid layout using Streamlit's native layout options and Markdown
    col_width = 12 // num_cols  # Calculate the width of each column
    grid_html = '<div class="grid-container">'
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            index = row * num_cols + col
            if index < num_recommendations:
                recommendation = recommendations[index]
                with cols[col]:
                    grid_html += '<div style="text-align: center;">'
                    grid_html += f'<img src="{recommendation["poster"]}" width="200">'
                    grid_html += f'<h4>{recommendation["name"]}</h4>'
                    grid_html += '</div>'
    grid_html += '</div>'

    st.markdown(grid_html, unsafe_allow_html=True)
