'''OpenAI API connector'''

import os
import logging

import openai
import streamlit as st

# Instantiate OpenAI with credentials from environment variables or streamlit secrets
openai_key = os.getenv('OPENAI_API_KEY') or st.secrets['OPENAI_API_KEY']
client = openai.OpenAI(api_key=openai_key)

# Suppress openai request/response logging
# Handle by manually changing the respective APIRequestor methods in the openai package
# Does not work hosted on Streamlit since all packages are re-installed by Poetry
# Alternatively (affects all messages from this logger):

logging.getLogger('openai').setLevel(logging.WARNING)

class OpenAI:
    '''OpenAI connector'''

    @staticmethod
    def moderate(prompt: str) -> bool:
        '''Call OpenAI GPT Moderation with text prompt
        Args:
            prompt (str): Text to moderate
        Returns:
            bool: True if text is safe, False otherwise
        '''
        try:
            response = client.moderations.create(input=prompt)
            return response.results[0].flagged
        
        except Exception as e:
            logging.error(f'OpenAI GPT Moderation failed: {e}')
            st.session_state.text_error = f'OpenAI GPT Moderation failed: {e}'

    @staticmethod
    def complete(
        prompt: str,
        model: str = 'gpt-3.5-turbo',
        temperature: float = 0.9,
        max_tokens: int = 50,
    ) -> str:
        '''
        Call OpenAI GPT Completion with text prompt
        Args:
            prompt (str): Text to complete
            model (str): Model to use
            temperature (float): Sampling temperature
            max_tokens (int): Maximum tokens to generate
        Returns:
            str: Completed text
        '''
        try:
            response = client.chat.completion.create(
                model=model,
                messages=[{'role': 'user', 'content': prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        
        except Exception as e:
            logging.error(f'OpenAI GPT Completion failed: {e}')
            st.session_state.text_error = f'OpenAI GPT Completion failed: {e}'

    @staticmethod
    def image(prompt: str) -> str:
        '''
        Call OpenAI CLIP Image with text prompt
        Args:
            prompt (str): Text to generate image from
        Returns:
            str: Image URL
        '''
        try:
            response = client.images.generate(
                prompt=prompt,
                model='dall-e-3',
                quality='standard',
                n=1,
                size='1024x1024',
            )
            return response.data[0].url
        
        except Exception as e:
            logging.error(f'OpenAI CLIP Image failed: {e}')
            st.session_state.text_error = f'OpenAI CLIP Image failed: {e}'
