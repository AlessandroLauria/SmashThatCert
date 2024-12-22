import streamlit as st

title = "SMASH THAT :blue[CERT]"
search_label = "Select your exam"
exam_simulator_button_txt = "Exam Simulation"
standard_exercises_button_txt = "Standard Exercises"

class Home():

    hide = False
    unique_button_clicked = -1

    exams_list: list = ["GCP Professional Cloud Developer", "exam2", "exam3"]
    exams_selected: str = None

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def _header(cls):
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
        cls._header()
        cls._exam_selection()

        if cls.exams_selected is not None:
            exam_clicked = cls._exam_simulator_button()
            exercises_clicked = cls._standard_exercises_button()

            if exam_clicked:
                cls.hide_page(True)
                cls.unique_button_clicked = 0
                st.rerun()

            elif exercises_clicked:
                cls.hide_page(True)
                cls.unique_button_clicked = 1
                st.rerun()

