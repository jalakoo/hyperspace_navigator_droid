
import streamlit as st
from droid import welcome_message, ask, DEFAULT_GREETING
from mapper import scan_of_galaxy, create_map
import pandas as pd
import altair as alt
import streamlit.components.v1 as components

# Static Image references
DROID_IMAGE_URL = 'https://res.cloudinary.com/dk0tizgdn/image/upload/t_Thumbnail/v1714600105/r2d2_jk4frc.png'
USER_IMAGE_URL = 'https://res.cloudinary.com/dk0tizgdn/image/upload/t_Thumbnail/v1714604482/poe_square_gkcdyy.png'

# Init message history
if "messages" not in st.session_state:
    st.session_state.messages = [
      {"role": "assistant", "content": DEFAULT_GREETING}
    ]

# HEADER
col1, col2 = st.columns([4,1])
with col1:
    st.title("Astro Droid Navigator")
with col2:
    st.image('https://res.cloudinary.com/dk0tizgdn/image/upload/t_Profile/v1714606886/benjamin-cottrell-astralanalyzer_frebud.png', width=80)

# Master star map using Altair map
# all_systems = scan_of_galaxy()
# all_systems_dict = [s.dict() for s in all_systems]
# all_systems_df = pd.DataFrame.from_dict(all_systems_dict)
# c = (
#    alt.Chart(all_systems_df)
#    .mark_circle()
#    .encode(x="X", y="Y", color="importance", tooltip=["name", "Region", "type"])
# ).interactive()
# st.altair_chart(c, use_container_width=True)

# Master map using SWGalaxyMap instead
components.iframe("http://www.swgalaxymap.com/", height=600)

# Display chat messages from history on app rerun
with st.empty().container():
    for message in st.session_state.messages:
        avatar_image = DROID_IMAGE_URL if message["role"] == "assistant" else USER_IMAGE_URL
        with st.chat_message(message["role"], avatar=avatar_image):
            st.markdown(message["content"], unsafe_allow_html=True)


user_input = st.chat_input(placeholder="Ask for a plot between 2 known Star Systems", key="user_input")

if user_input:
    with st.empty().container():
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user", avatar=USER_IMAGE_URL):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar=DROID_IMAGE_URL):
            with st.spinner('...'):
                message_placeholder = st.empty()
                droid_response, plot = ask(user_input, st.session_state.messages)
                if plot is not None:
                    plot_fig, _ = create_map(plot, show_plot=True)
                    st.pyplot(plot_fig)
                st.session_state.messages.append({"role": "assistant", "content": droid_response})
            
        message_placeholder.markdown(droid_response, unsafe_allow_html=True)