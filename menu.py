from pandas import DataFrame
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from cookie_manager import get_manager


cookie_manager = get_manager()

def menu(df: DataFrame):
  sidebar_choice = st.sidebar.selectbox("Menu", ("Movies", "Admin"))

  boxoffice = Image.open('boxoffice.png')
  popcorn = Image.open('popcorn.png')
  img1, img2 = st.columns(2)
  img1.image(boxoffice, width=500)
  img2.image(popcorn, width=200)

  if sidebar_choice == 'Movies':
    st.write('A list of movies')
    display_year = df['movie_year'].sort_values().max()-1
    start_year, end_year = st.select_slider(
    'Choose a year',
    options=df['movie_year'].sort_values().unique(),
    value=(df['movie_year'].sort_values().min(), display_year+1))
    st.dataframe(df[(df['movie_year'] >= start_year) & (df['movie_year'] <= end_year)])

    input_year = int(st.number_input('Insert a number', min_value=2000, max_value=2020, value=2020))
    
    st.header('Year ' + str(input_year) + ' compared to previous')
    col1, col2, col3 = st.columns(3)
    max_year_sum, difference_sum = sumOf(df, "domestic", input_year)
    col1.metric("Domestic", max_year_sum, difference_sum)

    max_year_sum, difference_sum = sumOf(df, "international", input_year)
    col2.metric("International", max_year_sum, difference_sum)

    max_year_sum, difference_sum = sumOf(df, "worldwide", input_year)
    col3.metric("Worldwide", max_year_sum, difference_sum)

    fig = go.Figure(data=[
        go.Bar(name='Worlwide', x=df['movie_year'], y=df['worldwide']),
        go.Bar(name='Domestic', x=df['movie_year'], y=df['domestic']),
        go.Bar(name='International', x=df['movie_year'], y=df['international'])
    ])
    st.plotly_chart(fig, use_container_width=True)

def sumOf(df: DataFrame, sum_column: str, year: int): 
  max_year_sum = df[df['movie_year'] == year][sum_column].sum()
  previous_year_sum = df[df['movie_year'] == (year-1)][sum_column].sum()
  difference_sum =  (max_year_sum - previous_year_sum) / previous_year_sum * 100
  return round(max_year_sum, 2), round(difference_sum, 2)