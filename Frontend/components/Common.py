import streamlit as st
import os
from pathlib import Path
from streamlit_extras.bottom_container import bottom
from streamlit_extras.buy_me_a_coffee import button

icon_path = os.path.join(Path(__file__).parent.parent.parent, "images", "smash_that_cert_icon.png")

def header_bar():
    left_col, middle_1_col, right = st.columns(3)

    left_col.text("Created by Alessandro Lauria")
    right.page_link("https://discord.gg/Xkb4maMUEb", label="Request a new exam on Discord", icon="🚀")
    with bottom():
        button(username="learnsodas", floating=False, width=500)