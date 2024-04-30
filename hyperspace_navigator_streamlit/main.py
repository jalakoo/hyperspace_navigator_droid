
import streamlit as st
from droid import welcome_message, ask, DEFAULT_GREETING
from mapper import create_map
import matplotlib.pyplot as plt

# Init message history
if "messages" not in st.session_state:

    st.session_state.messages = [
      {"role": "ai", "content": DEFAULT_GREETING}
    ]

# Display chat messages from history on app rerun
with st.empty().container():
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)


user_input = st.chat_input(placeholder="Ask for a plot between 2 known Star Systems", key="user_input")

if user_input:
  with st.empty().container():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
      st.markdown(user_input)

    with st.chat_message("ai"):
      with st.spinner('...'):
        message_placeholder = st.empty()
        droid_response, plot = ask(user_input, st.session_state.messages)
        if plot is not None:
            fig = create_map(plot)
            st.pyplot(fig)
        
    message_placeholder.markdown(droid_response, unsafe_allow_html=True)
    