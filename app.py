#https://github.com/kinosal/tweet/tree/main
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

    