import pandas as pd
import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(
    page_title='Aadil_Book_Recommendation',
    layout='wide'
)
st.title('Book Recommender System')

popular_df = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_scores = pd.read_pickle('similarity_scores.pkl')

book_name = list(popular_df['Book-Title'].values)
author=list(popular_df['Book-Author'].values)
image=list(popular_df['Image-URL-M'].values)
votes=list(popular_df['num_ratings'].values)
rating=list(popular_df['avg_rating'].values)

selected_book_name = st.selectbox('Select your favorite book 👇', popular_df['Book-Title'].values)

def recommend(book_name):
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:11]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    
    return data

if st.button('Recommend'):
    data = recommend(selected_book_name)
    for i in data:
        col1, col2 = st.columns([1,6])
        with col1:
            st.image(i[2])
            
        with col2:
            st.subheader(i[0])
            st.write('Author',i[1])
