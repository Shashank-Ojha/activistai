import streamlit as st
from streamlit_chat import message

import time
import activist_ai as act



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
    st.session_state['query_fn'] = None

if submit_button:
    # st.session_state['saved_verbose'] = verbose

    loading_placeholder.text("Fetching personal agent for this task...")
    st.session_state['query_fn'] = act.query_fn()
    loading_placeholder.text("Assistant is ready for service!")
    time.sleep(0.5)
    loading_placeholder.empty()

    st.session_state.messages = []

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