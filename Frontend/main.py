import streamlit as st
from pages.Home import Home
from pages.ExercisePage import ExamSimulator, StandardExercise


#if not Home.have_to_hide():
#    Home.homepage()

st.switch_page("pages/Home.py")

# if Home.unique_button_clicked == 0:
#     if ExamSimulator.exam_selected is None:
#         exam = Home.exams_selected.split("-")[0].strip()
#         ExamSimulator.set_exam(exam)
#     ExamSimulator.homepage()
#
# if Home.unique_button_clicked == 1:
#     if StandardExercise.exam_selected is None:
#         exam = Home.exams_selected.split("-")[0].strip()
#         StandardExercise.set_exam(exam)
#     StandardExercise.homepage()