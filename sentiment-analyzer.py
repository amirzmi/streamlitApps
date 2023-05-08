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
st. set_page_config(layout="wide") 
####################
### INTRODUCTION ###
####################
#row0_spacer1, row0_1, row0_spacer2 = st.columns((.1, 3.2, .1))
#row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
row0_spacer1, row0_1, row0_spacer2 = st.columns((.1, 3.2, .1))
with row0_1:
    st.title('SRanalyser: Steam Reviews Analyser')
#with row0_2:
    #st.text("")
    #st.text("")
    #st.subheader('App created by [Amir Azmi](https://www.linkedin.com/in/amir-azmi-064a62261/)')
#row00_spacer1, row00_1, row00_spacer2 = st.columns((.1, 3.2, .1))
#with row00_1:

row1_spacer1, row1_1, row1_spacer2 = st.columns((.1, 3.2, .1))
with row1_1:
    st.subheader('App created by [Amir Azmi](https://www.linkedin.com/in/amir-azmi-064a62261/)')
    st.markdown('Hello there! This is my Final Year Project and the title for this project: Web-based Sentiment analyser for reviews on STEAM Platform.')
    st.markdown('You can find the source code for this project in the [SRAnalyser GitHub Repository](https://github.com/amirzmi/SRAnalyser).')
    
####################
### SELECTION    ###
####################
st.set_option('deprecation.showfileUploaderEncoding', False)

st.sidebar.header("ANALYSE SENTIMENT")
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
row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3, row2_spacer4= st.columns((.2, 2.2, .2, 2.5, .2, 2.2, .2))
with row2_1:
   st.header('Dashboard')
with row2_2:
   st.header('') 
with row2_3:
   st.header('')

st.header('')
count_positive = 0
count_negative = 0
count_neutral  = 0

if uploaded_file is not None:

        
    input_df = pd.read_csv(uploaded_file)
    
    row44_spacer1, row44_1, row44_spacer2, row44_2, row44_spacer3  = st.columns((.2, 6, .0, 2.3, .0))
    with row44_1:
        st.markdown('<h5>ENTERED INPUT</h5>', unsafe_allow_html=True) 
        st.write(input_df)
    with row44_2:
        st.markdown('<h5>SENTIMENT RESULT</h5>', unsafe_allow_html=True) 
        
    for i in range(input_df.shape[0]):
        
        input = str(input_df.iloc[i])
                    
        url = 'https://sranalyser.herokuapp.com/classify/?text='+str(input_df.iloc[i])
        r = requests.get(url)
        
        result = r.json()["text_sentiment"]
        
        with row44_2:
            st.markdown(result)
            
        if result=='recommend':
            count_positive+=1
        elif result=='not recommend':
            count_negative+=1
        else:
            count_neutral+=1 
            
            
    x = ["Recommendation", "Not Recommendation", "Neutral"]
    y = [count_positive, count_negative, count_neutral]
    row55_spacer1, row55_1, row55_spacer2 = st.columns((.2, 7.1, .2))
    with row55_1: 
        st.markdown('')
        layout = go.Layout(
            title = 'Multiple Reviews Analysis',
            xaxis = dict(title = 'Category'),
            yaxis = dict(title = 'Number of reviews'),)

        fig.update_layout(dict1 = layout, overwrite = True)
        fig.add_trace(go.Bar(name = 'Multi Reviews', x = x, y = y))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('') 
        st.markdown('<div style="text-align: justify;"><h5> Interpretation:  </h5></div>', unsafe_allow_html=True)
        if count_positive>count_negative:
            st.markdown("""= ✅ Great work there! The majority of people recommended the games. 😃""")
        elif count_negative>count_positive:
            st.markdown("""= ❌ Try improving your games! The majority of people didn't recommend your games up to the mark. 😶""")
        else:
            st.markdown("""= 🆗 Good Work there, but there's room for improvement! Majority of people have neutral reactions. 😶""")

elif single_review:
    url = 'https://sranalyser.herokuapp.com/classify/?text='+single_review
    r = requests.get(url)
    result = r.json()["text_sentiment"]
    
    ### BELOW DASHBOARD ###
    #row3_spacer1, row3_1, row3_spacer2 = st.columns((.2, 7.1, .2))
    #with row3_1:
        #st.subheader('Single Review Analysis')

    row4_spacer1, row4_1, row4_spacer2, row4_2, row4_spacer3  = st.columns((.2, 4.4, .4, 2.3, .2))
    with row4_1:
        st.markdown('<h5>ENTERED INPUT</h5>', unsafe_allow_html=True) 
        st.markdown(single_review) 
    with row4_2:
        st.markdown('<h5>SENTIMENT RESULT</h5>', unsafe_allow_html=True) 
        st.markdown(result)
        
    row5_spacer1, row5_1, row5_spacer2 = st.columns((.2, 7.1, .2))
    with row5_1:
        st.text('')
        st.markdown('<div style="text-align: justify;"><h5> Interpretation:  </h5></div>', unsafe_allow_html=True)
        if result=='recommend':
            st.markdown('<div style="text-align: justify;"><h6> = ✅ Great work there! You got a positive review. That means the gamer recommended your games. 😃</h6></div>', unsafe_allow_html=True)
        elif result=='not recommend':
            st.markdown('<div style="text-align: justify;"><h6> = ❌ Hmmm... You got a negative review... Looks like the gamers are not satisfied with your games. 😔</h6></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: justify;"><h6> = 🆗 Good work there, but there is room for improvement! You got a neutral review. 😶</h6></div>', unsafe_allow_html=True)
       
else:
    row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
    with row6_1:
        st.markdown('')
        st.markdown('<div style="text-align: justify;"><h5>⬅ Enter user input from the sidebar to analyse sentiment of the review.</h5></div>', unsafe_allow_html=True)



