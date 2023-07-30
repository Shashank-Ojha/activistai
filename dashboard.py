import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import threading
import time

title = "Title"

def thread_1():                     
  for i in range(5):
    global title
    title = f"this is thread {i}"
    st.experimental_rerun()
    time.sleep(3)

# creating a thread
T = threading.Thread(target = thread_1)
 
# change T to daemon
T.setDaemon(True) 

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)
ax.set_title('Histogram')

st.pyplot(fig)