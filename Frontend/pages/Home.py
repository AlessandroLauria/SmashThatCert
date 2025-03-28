import streamlit as st
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from Backend.ExamHandler import ExamMetadata
from components.Common import header_bar
from streamlit_extras.buy_me_a_coffee import button
from Libs.ConfigHandler import ConfigHandler

icon_path = os.path.join(Path(__file__).parent.parent.parent, "images", "smash_that_cert_icon.png")
main_config = ConfigHandler(os.path.join(str(Path(__file__).parent.parent.parent),"Config"), "main_config")

title = "SMASH THAT :blue[CERT]"
search_label = "Select your exam"
exam_simulator_button_txt = "Exam Simulation"
standard_exercises_button_txt = "Standard Exercises"

st.set_page_config(
    page_title="Smash That Cert",
    page_icon=icon_path,
    layout="centered",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

class Home():

    hide = False
    unique_button_clicked = -1

    exams_list: list = ExamMetadata.get_exams_list() #["GCP Professional Cloud Developer", "exam2", "exam3"]
    exams_selected: str = None

    left_col, middle_col, right_col = st.columns(3)

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def _logo(cls):
        cls.left_col.image(icon_path, width=100)

    @classmethod
    def _header(cls):
        cls.left_col.text(f"Created by Alessandro Lauria\nV{main_config.config['version']}")
        cls.right_col.page_link("https://discord.gg/Xkb4maMUEb", label="Request a new exam on Discord", icon="🚀")
        st.header(title, divider="blue")

    @classmethod
    def _exam_selection(cls):
        cls.exams_selected = st.selectbox(search_label, cls.exams_list, index=None)

    @classmethod
    def _exam_simulator_button(cls):
        return st.button(exam_simulator_button_txt, use_container_width=True)

    @classmethod
    def _standard_exercises_button(cls):
        return st.button(standard_exercises_button_txt, use_container_width=True)

    @classmethod
    def hide_page(cls, bool):
        cls.hide = bool

    @classmethod
    def have_to_hide(cls):
        return cls.hide

    @classmethod
    def homepage(cls):
        #cls._logo()
        header_bar()
        cls._header()

        cls._exam_selection()

        if cls.exams_selected is not None:
            exam_clicked = cls._exam_simulator_button()
            exercises_clicked = cls._standard_exercises_button()

            if exam_clicked:
                st.session_state["exams_selected"] = cls.exams_selected
                st.session_state["exercise_page_type"] = "ExamSimulator"
                st.switch_page("pages/ExercisePage.py")

            elif exercises_clicked:
                st.session_state["exams_selected"] = cls.exams_selected
                st.session_state["exercise_page_type"] = "StandardExercise"
                st.switch_page("pages/ExercisePage.py")


st.cache_resource.clear()
Home.homepage()

