import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import pickle
import keywords_util
import os

title = "Title"

keyword_counts = {}
# Load Pickle File
if os.path.isfile('counts.pkl'):
  with open('counts.pkl', 'rb') as file:
    keyword_counts = pickle.load(file)

plt = keywords_util.plot_key_words(keyword_counts)

st.pyplot(plt)