import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from Backend.ExamHandler import ExamHandler

previous_button_text = "Previous"
next_button_text = "Next"
quit_button_text = "Quit"

class ExcercisePage():

    title = ""
    hide = True

    exam_selected: str = None

    def __init__(self):
        pass

    @classmethod
    def set_exam(cls, exam):
        cls.exam_selected = exam

    @classmethod
    def hide_page(cls, bool):
        cls.hide = bool

    @classmethod
    def have_to_hide(cls):
        return cls.hide

    @classmethod
    def homepage(cls):
        st.header(cls.title, divider="blue")

        st.subheader("this is the text of the first question, choose between all the options and make sure to respond correctly. Have a good luck")
        st.divider()
        answerer = st.radio(
            "What's your favorite movie genre",
            ["Option 1", "Option 2", "Option 3", "Option 4"],
        )

        left, middle_1, middle_2, middle3, right = st.columns(5)

        if left.button(previous_button_text, use_container_width=True, type="secondary"):
            pass
        if middle_1.button(next_button_text, use_container_width=True, type="primary"):
            pass
        if right.button(quit_button_text, use_container_width=True, type="tertiary"):
            pass

        st.progress(5, text="5/60")

        st.page_link("your_app.py", label="Home", icon="🏠")


class ExamSimulator(ExcercisePage):

    title = "Exam Simulator"
    hide = True

    def __init__(self):
        pass

    @classmethod
    def set_exam(cls, exam):
        super().set_exam(exam)
        ExamHandler(exam, 60, True)

class StandardExercise(ExcercisePage):

    title = "Standard Exercises"
    hide = True

    def __init__(self):
        pass

    @classmethod
    def set_exam(cls, exam):
        super().set_exam(exam)
        ExamHandler(exam)

