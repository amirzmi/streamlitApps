import streamlit as st
import pandas as pd
import numpy as np
import requests
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
from pandas.io.json import json_normalize
import pickle

fig = go.Figure()

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('StR - STEAM Reviews Analyser')
with row0_2:
    st.text("")
    st.subheader('Created by [Amir Azmi](https://www.linkedin.com/in/amir-azmi-064a62261/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Hello there! This is my Final Year Project as title: Web-based Sentiment analyser for reviews on STEAM Platform")
    st.markdown("You can find the source code for this project in the [SRAnalyser GitHub Repository](https://github.com/amirzmi/SRAnalyser)")

st.set_option('deprecation.showfileUploaderEncoding', False)

st.sidebar.header("""#ANALYSE SENTIMENT""")

st.sidebar.subheader('Single Review Analysis')
single_review = st.sidebar.text_input('Enter your single review below:')

st.sidebar.subheader('Mutiple Reviews Analysis')
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

count_positive = 0
count_negative = 0
count_neutral = 0
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
    for i in range(input_df.shape[0]):
        url = 'https://sranalyser.herokuapp.com/classify/?text='+str(input_df.iloc[i])
        r = requests.get(url)
        result = r.json()["text_sentiment"]
        if result=='positive':
            count_positive+=1
        elif result=='negative':
            count_negative+=1
        else:
            count_neutral+=1 

    x = ["Positive", "Negative", "Neutral"]
    y = [count_positive, count_negative, count_neutral]

    if count_positive>count_negative:
        st.write("""# Great Work there! Majority of people recommended the games 😃""")
    elif count_negative>count_positive:
        st.write("""# Try improving your product! Majority of people didn't recommended your games upto the mark 😔""")
    else:
        st.write("""# Good Work there, but there's room for improvement! Majority of people have neutral reactions to listed games 😶""")
        
    layout = go.Layout(
        title = 'Multiple Reviews Analysis',
        xaxis = dict(title = 'Category'),
        yaxis = dict(title = 'Number of reviews'),)
    
    fig.update_layout(dict1 = layout, overwrite = True)
    fig.add_trace(go.Bar(name = 'Multi Reviews', x = x, y = y))
    st.plotly_chart(fig, use_container_width=True)

elif single_review:
    url = 'https://sranalyser.herokuapp.com/classify/?text='+single_review
    r = requests.get(url)
    result = r.json()["text_sentiment"]
    if result=='positive':
        st.write("""# Great Work there! You got a Positive Review 😃. The user recommended your games""")
    elif result=='negative':
        st.write("""# Try improving your product! You got a Negative Review 😔. Look like the user do not recommend your games... 😔 """)
    else:
        st.write("""# Good Work there, but there's room for improvement! You got a Neutral Review 😶 """)

else:
    st.write("""# ⬅ Enter user input from the sidebar to see the sentiment of the review.""")

st.sidebar.subheader("""Created with 💖 by Amir Azmi""")

