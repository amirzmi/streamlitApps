import streamlit as st
import pandas as pd
import numpy as np
import requests
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
from pandas.io.json import json_normalize
import pickle

####################
### INTRODUCTION ###
####################
row0_spacer1, row0_1, row0_spacer2 = st.columns((.1, 3.2, .1))
with row0_1:
    st.title('SRAnalyser - Steam Reviews Analyser')
    
row00_spacer1, row00_1, row00_spacer2 = st.columns((.1, 3.2, .1))
with row00_2:
    st.subheader('App created by [Amir Azmi](https://www.linkedin.com/in/amir-azmi-064a62261/)')
    
row1_spacer1, row1_1, row1_spacer2 = st.columns((.1, 3.2, .1))
with row1_1:
    st.markdown('Hello there! This is my Final Year Project and the title for this project: Web-based Sentiment analyser for reviews on STEAM Platform.</div>')
    st.markdown('You can find the source code for this project in the [SRAnalyser GitHub Repository](https://github.com/amirzmi/SRAnalyser).')
    
####################
### SELECTION    ###
####################
st.set_option('deprecation.showfileUploaderEncoding', False)

st.sidebar.header("        ANALYSE SENTIMENT        ")
st.sidebar.text('')
st.sidebar.text('')
#st.sidebar.markdown('**Single Review Analysis**')
single_review = st.sidebar.text_input(' Enter your single review 👇')
st.sidebar.text('')
#st.sidebar.markdown('**Multiple Review Analysis**')
uploaded_file = st.sidebar.file_uploader(" Upload your input CSV file 👇", type=["csv"])
st.sidebar.text('')
#st.sidebar.subheader("""Created with 💖 by Amir Azmi""")

### SEE DATA ###
st.header('')
st.header('________________________________________________________________________________________________________________')
row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3, row2_spacer4= st.columns((.2, 2.2, .2, 2.5, .2, 2.2, .2))
with row2_1:
   st.header('')
with row2_2:
   st.header('DASHBOARD') 
with row2_3:
   st.header('')
    
count_positive = 0
count_negative = 0
count_neutral  = 0

if uploaded_file is not None:
    row7_spacer1, row7_1, row7_spacer2 = st.columns((.2, 7.1, .2))
    with row7_1:
        st.subheader('Multiple Review Analysis')
        
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
    
    row8_spacer1, row8_1, row8_spacer2 = st.columns((.2, 7.1, .2))
    with row8_1:
        #st.subheader('Multiple Review Analysis')    
    if count_positive>count_negative:
        st.markdown("""#Great Work there! Majority of people recommended the games. 😃""")
    elif count_negative>count_positive:
        st.markdown("""#Try improving your games! Majority of people didn't recommended your games upto the mark... 😔""")
    else:
        st.markdown("""#Good Work there, but there's room for improvement! Majority of people have neutral reactions. 😶""")
        
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
    
    ### BELOW DASHBOARD ###
    row3_spacer1, row3_1, row3_spacer2 = st.columns((.2, 7.1, .2))
    with row3_1:
        #st.subheader('Single Review Analysis')

    row4_spacer1, row4_1, row4_spacer2, row4_2, row4_spacer3  = st.columns((.2, 4.4, .4, 2.3, .2))
    with row4_1:
        st.markdown('**Entered Input**') 
        st.markdown(' = '+single_review) 
    with row4_2:
        st.markdown('**Result**') 
        st.markdown(' = '+result)
        
    row5_spacer1, row5_1, row5_spacer2 = st.columns((.2, 7.1, .2))
    with row5_1:
        if result=='positive':
            st.markdown('<div style="text-align: justify;"><h3>Great Work there! You got a Positive Review. That mean the gamer recommended your games. 😃</h3></div>', unsafe_allow_html=True)
        elif result=='negative':
            st.markdown('<div style="text-align: justify;"><h3>Hmmm... You got a Negative Review... Look like the gamer do not satisfy with your game... 😔</h3></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: justify;"><h3>Good Work there, but there is room for improvement! You got a Neutral Review. 😶</h3></div>', unsafe_allow_html=True)
       
else:
    row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
    with row6_1:
        st.markdown('')
        st.markdown("""# ⬅ Enter user input from the sidebar to analyse sentiment of the review.""")



