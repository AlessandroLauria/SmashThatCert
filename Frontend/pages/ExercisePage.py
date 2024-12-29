import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from Backend.ExamHandler import ExamHandler

question_number_text = "Question #"
previous_button_text = "Previous"
next_button_text = "Next"
quit_button_text = "Quit"
submit_exam_text = "Submit Exam"
show_correct_answare_text = "Show Correct Answare"

mapping_c2n = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
}

class ExcercisePage():

    title = ""
    hide = True

    exam_selected: str = None
    exam_handler = None

    # question vars
    question_text = ""
    question_options_text = "Options"
    question_options = []
    num_current_question = 1
    total_num_question = 1
    original_question_link = None

    def __init__(self):
        pass

    @classmethod
    def set_exam(cls, exam):
        print("Setting exam")
        cls.exam_selected = exam

    @classmethod
    def hide_page(cls, bool):
        cls.hide = bool

    @classmethod
    def have_to_hide(cls):
        return cls.hide

    @classmethod
    def _question_formatter(cls, question):
        cls.question_text = question["question_text"]
        cls.question_options = question["question_options"]
        cls.original_question_link = question["link"]
        cls.num_current_question = cls.exam_handler.get_current_question_num()
        cls.total_num_question = cls.exam_handler.get_total_num_questions()

    @classmethod
    def _change_question(cls, direction=1): # 1 is next question, -1 is previous question
        if cls.exam_handler is not None:
            current_question = None
            if direction == 1:
                current_question = cls.exam_handler.next_question()
            elif direction == -1:
                current_question = cls.exam_handler.previous_question()

            if current_question is not None:
                cls._question_formatter(current_question)
                st.rerun()

    @classmethod
    def _button_row(cls):
        cls.left, cls.middle_1, cls.middle_2, cls.middle3, cls.right = st.columns(5)

        if cls.left.button(previous_button_text, use_container_width=True, type="secondary"):
            cls._change_question(-1)
        if cls.middle_1.button(next_button_text, use_container_width=True, type="primary"):
            cls._change_question(1)
        if cls.middle3.button(quit_button_text, use_container_width=True, type="tertiary"):
            st.switch_page("pages/Home.py")

    @classmethod
    def homepage(cls):
        if cls.exam_selected is None:
            cls.set_exam(st.session_state["exams_selected"].split("-")[0].strip())
        st.header(cls.title, divider="blue")

        st.subheader(f"{cls.exam_selected} - {question_number_text}{cls.num_current_question+1}")
        st.text(cls.question_text)
        st.divider()

        current_question = cls.exam_handler.get_current_question_info()
        option_selected = st.radio(
            cls.question_options_text,
            cls.question_options,
            index=current_question["option_selected"] if current_question["option_selected"] is not None else None
        )

        cls.exam_handler.set_option_selected(cls.exam_handler.get_current_question_num()
                                             ,cls.question_options.index(option_selected)
                                             if option_selected is not None
                                             else None)

        st.markdown("#") # empty space

        cls._button_row()

        st.progress(
            (cls.num_current_question+1)/cls.total_num_question,
            text=f"{cls.num_current_question+1}/{cls.total_num_question}"
        )

        st.divider()
        if cls.original_question_link is not None:
            st.page_link(cls.original_question_link, label=cls.original_question_link, icon="🔗")


class ExamSimulator(ExcercisePage):

    title = "Exam Simulator"
    hide = True

    @classmethod
    def set_exam(cls, exam):
        super().set_exam(exam)
        cls.exam_handler = ExamHandler(exam, 60, True)
        cls._question_formatter(cls.exam_handler.next_question())

    @classmethod
    def _button_row(cls):
        super()._button_row()

        if cls.right.button(submit_exam_text, use_container_width=True, type="primary"):
            results, questions = cls.exam_handler.collect_results()
            st.session_state["exam_results"] = results
            st.session_state["questions_submitted"] = questions
            st.switch_page("pages/RecapPage.py")

class StandardExercise(ExcercisePage):

    title = "Standard Exercises"
    hide = True

    @classmethod
    def set_exam(cls, exam):
        super().set_exam(exam)
        cls.exam_handler = ExamHandler(exam)
        cls._question_formatter(cls.exam_handler.next_question())

    @classmethod
    def _button_row(cls):
        super()._button_row()

        if cls.right.button(show_correct_answare_text, use_container_width=True, type="primary"):
            with st.container(border=True):
                question = cls.exam_handler.get_current_question_info()
                correct_answare_index = mapping_c2n[question["most_voted"]]
                st.text(cls.question_options[correct_answare_index])
                st.divider()


exercise_page = None

@st.cache_resource
def get_page():
    exercise_page = None
    if st.session_state["exercise_page_type"] == "ExamSimulator":
        exercise_page = ExamSimulator
    elif st.session_state["exercise_page_type"] == "StandardExercise":
        exercise_page = StandardExercise

    return exercise_page

if "exercise_page_type" in st.session_state.keys():
    get_page().homepage()