import streamlit as st
from streamlit_chat import message

import time
import activist_ai as act
import keywords_util
import pickle
import os

# Setting page title and header
st.set_page_config(page_title="Activist AI", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'> Activist AI - chatbot 😬</h1>", unsafe_allow_html=True)

# Loading placeholder.
loading_placeholder = st.empty()

# Sidebar - let user choose data inputs and model. Let user clear the current conversation
st.sidebar.title("Sidebar")
# Data Inputs.
# project_id = st.sidebar.text_input("Project ID", value="jira-168618")

# Verbose mode
# verbose = st.sidebar.checkbox("Verbose", value=False)

# Submit all configs
submit_button = st.sidebar.button("Submit")

# Clear button
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# TODO: Should subclass and override method to prevent printing entire prompt.
# st_callback = CustomStreamlitCallbackHandler() if verbose else None

if 'query_fn' not in st.session_state:
    st.session_state['query_fn'] = act.query_fn()

if submit_button:
    email_text = "Traffic light accidents are horrible."
    keywords = keywords_util.extract_key_words(email_text)

    keyword_counts = {}
    # Load Pickle File
    if os.path.isfile('counts.pkl'):
      with open('counts.pkl', 'rb') as file:
        keyword_counts = pickle.load(file)

    for kw in keywords:
        key = kw.strip().lower()
        if key in keyword_counts:
            keyword_counts[key] += 1
        else:
            keyword_counts[key] = 1

    # Save Pickle File
    with open('counts.pkl', 'wb') as file:
      pickle.dump(keyword_counts, file, protocol=pickle.HIGHEST_PROTOCOL)


if clear_button:
    # Clear history.
    st.session_state.messages = []

# ----------- Chat UI Code  --------------

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # response = f"Echo: {prompt}"
    response = st.session_state['query_fn'](prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})