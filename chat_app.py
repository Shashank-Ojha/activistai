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
submit_button = st.sidebar.button("Create Email")

# Clear button
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# TODO: Should subclass and override method to prevent printing entire prompt.
# st_callback = CustomStreamlitCallbackHandler() if verbose else None

if 'query_fn' not in st.session_state:
    st.session_state['query_fn'] = act.query_fn()

if submit_button:
    last_msg = st.session_state.messages[-1]["content"]

    email_template_prompt = f"""given this response of {last_msg}, your job is to make an email to the follow CSV list of departments of San Francisco:

    Department Name, Email, Phone Number

    311 Customer Service Center, 311@sfgov.org, 415-701-2311

    Adult Probation Department, apd@sfgov.org, 415-553-1750

    Airport, info@flysfo.com, 650-821-8211

    Animal Care and Control, acc@sfgov.org, 415-554-6364

    Department of Aging and Adult Services, daas@sfgov.org, 415-355-6700

    Department of Elections, sfvote@sfgov.org, 415-554-4375

    Department of Emergency Management, dem@sfgov.org, 415-558-2700

    Department of Police Accountability, dpa@sfgov.org, 415-241-7711

    Department of Public Health, dph@sfdph.org, 415-554-2500

    Department of Public Works, dpw@sfdpw.org, 415-554-6920

    Fire Department, sffireadmin@sfgov.org, 415-558-3200

    Human Resources, dhr@sfgov.org, 415-557-4800

    Municipal Transportation Agency, sfmta@sfmta.com, 415-701-2311

    Police Department, sfpd.online@sfgov.org, 415-575-4444

    The brackets, [], should be be prefilled with the CSV values. The values inside the <text> xml tag will be interpreted by you and respond and be formatted in plain text. Use the above CSV values to fillout an email in the following format:

    email: To [Email]

    Subject line: <text>make a description that has an overview of the response

    Body: Hi [Department Name] without brackets around the name,

    <text>Draft an email based on the response of the crime rate of the SOMA district in SF to be sent to the department that closely matches this response and closes with a signature from ActivistAi without brackets around the name</text>
    """
    email = act.claude_chat(email_template_prompt)

    st.session_state.messages.append({"role": "assistant", "content": email})
  
    keywords = keywords_util.extract_key_words(email)

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