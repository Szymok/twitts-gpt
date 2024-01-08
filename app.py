'''Streamlit app to generate Tweets'''

# import from standard library
import logging
import random
import re

# import from third-party
import streamlit as st
import streamlit.components.v1 as components
import streamlit_analytics

#import modules
import tweets as twe
import oai

# Configure logger
logging.basicConfig(
    format='\n%(asctime)s\n%(message)s', level=logging.INFO, force=True
)

# Define functions
def generate_tweets(topic: str, mood: str = '', style: str = ''):
    '''
    Generate tweets based on topic and mood
    '''

    if st.session_state.n_requests >= 5:
        st.session_state.text_error = 'Too many requests. Please try again later.'
        logging.info(f'Session requests limit reached : {st.session_state.n_requests}')
        st.session_state.n_requests = 1
        return
    
    st.session_state.tweet = ''
    st.session_state.image = ''
    st.session_state.text_error = ''

    if not topic:
        st.session_State.text_error = 'Please enter a topic'
        return
    
    with text_spinner_placeholder:
        with st.spinner('Please wait while your tweet is being generated...'):
            mood_prompt = f'{mood} ' if mood else ''
            if style:
                twitter = twe.Tweets(account=style)
                tweets = twitter.fetch_tweets()
                tweets_prompt = '\n\n'.join(tweets)
                prompt = (
                    f'Write a {mood_prompt}Tweet about {topic} in less than 120 character '
                    f'and in the style of the following Tweets: \n\n{tweets_prompt}\n\n'
                )
            else:
                prompt = f'Write a {mood_prompt}Tweet about {topic} in less than 120 characters:\n\n'

            openai = oai.Openai()
            flagged = openai.moderate(prompt)
            mood_output = f', Mood: {mood}' if mood else ''
            style_output = f'. Style: {style}' if style else ''
            if flagged:
                st.session_state.text_error = 'Input flagged as inappropriate. Please try again.'
                logging.info(f'Topic: {topic}{mood_output}{style_output}\m')
                return
            else:
                st.session_state.text_error = ''
                st.session_state.n_requests += 1
                streamlit_analytics.start_tracking()
                st.session_state.tweet = (
                    openai.complete(prompt=prompt).strip().replace('"', "")
                )
                logging.info(
                    f'Topic: {topic}{mood_output}{style_output}\n'
                    f'Tweet: {st.session_state.tweet}'
                )

