import streamlit as st
from Home import Home
from ExercisePage import ExamSimulator, StandardExercise


if not Home.have_to_hide():
    Home.homepage()

if Home.unique_button_clicked == 0:
    if ExamSimulator.exam_selected is None:
        ExamSimulator.set_exam(Home.exams_selected)
    ExamSimulator.homepage()

if Home.unique_button_clicked == 1:
    if StandardExercise.exam_selected is None:
        StandardExercise.set_exam(Home.exams_selected)
    StandardExercise.homepage()