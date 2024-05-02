
import streamlit as st
from droid import welcome_message, ask, DEFAULT_GREETING
from mapper import create_map

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

# Master star map from swgalaxymap
display = f'<iframe src="https://hbernberg.carto.com/builder/6650a85d-b115-4680-ab97-721bf8a41a90/embed" width="100%" height="600" frameborder="0" allowfullscreen="allowfullscreen"></iframe><p><cite><small>Embedded interactive map by <a href="http://www.swgalaxymap.com/">SWGalaxyMap</a>. Star Wars is a trademark and copyright of Lucasfilm and Disney.</small></cite></p>'
st.markdown(display, unsafe_allow_html=True)

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