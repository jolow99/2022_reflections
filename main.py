import pandas as pd 
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# @st.cache(persist=True)
def load_data():
    sheet_url = st.secrets["private_gsheets_url"]
    query = f'SELECT * FROM " {sheet_url} "'
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    df = pd.DataFrame(rows)
    return df

st.set_option('deprecation.showPyplotGlobalUse', False)
df = load_data()

# 1. Introduction
st.title("My Daily Reflections In 2022")
st.write("This is a simple app that I made to visualise my daily reflections, a habit I picked up at the start of the year.")
st.markdown("---")

# extend STOPWORDS list with names of friends and other words that I don't want to appear in the wordcloud
STOPWORDS.add('shin')
STOPWORDS.add('getPID')
STOPWORDS.add('jon')
STOPWORDS.add('aaron')
STOPWORDS.add('jon')
STOPWORDS.add('asio')
STOPWORDS.add('nirat')

# 2. Storyworthy Visualisation
st.subheader("Storyworthy Moments of My Days")
story_col = df['Storyworthy']
story_col = story_col.dropna()
story_col = story_col[story_col.str.len() > 2]

# Streamlit slider which defaults to 10
max_story_words = st.slider("Max number of words", 10, 100, 10, key="story")

# make a wordcloud of the Storyworthy column
wordcloud = WordCloud(width = 800, height = 400,
                background_color ='white',
                stopwords = STOPWORDS,
                max_words = max_story_words,
                min_font_size = 10).generate(str(story_col))

# Display the generated image:
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
st.pyplot()

st.markdown("---")


# 3. Grateful Visualisation
st.subheader("What I'm grateful for")
grateful_col = df['Grateful']
grateful_col = grateful_col.dropna()
grateful_col = grateful_col[story_col.str.len() > 2]

# Streamlit slider which defaults to 10
max_grateful_words = st.slider("Max number of words", 10, 100, 10, key="grateful")

# make a wordcloud of the Grateful column
wordcloud = WordCloud(width = 800, height = 400,
                background_color ='white',
                stopwords = STOPWORDS,
                max_words = max_grateful_words,
                min_font_size = 10).generate(str(grateful_col))

# Display the generated image:
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
st.pyplot()

st.markdown("---")



# 4. Day Rating
st.subheader("Rating my day from 1 to 10")
score_col = df['Overall']
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Average", value=round(score_col.mean(),1))
col2.metric(label="Median", value=score_col.median())
col3.metric(label="Mode", value=score_col.mode()[0])
col4.metric(label="Standard Deviation", value=round(score_col.std(),1))
st.line_chart(score_col)