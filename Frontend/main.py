import streamlit as st
import sys
import os
from pathlib import Path
from pages.Home import Home
from pages.ExercisePage import ExamSimulator, StandardExercise

#icon_path = os.path.join(Path(__file__).parent.parent, "images", "smash_that_cert_icon.png")
#st.set_page_config(
#    page_title="Smash That Cert",
#    page_icon=icon_path,
#    layout="wide",
#)

st.switch_page("pages/Home.py")