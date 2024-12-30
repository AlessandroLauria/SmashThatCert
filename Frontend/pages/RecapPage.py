import streamlit as st
import matplotlib.pyplot as plt

title_page_text = "Recap"
quit_button_text = "Home"

class QuestionCard():

    def __init__(self, question):
        self.question_text = question["question_text"]
        self.question_options = question["question_options"]
        self.correct_answare = question["most_voted"]
        self.given_answare = question["option_selected"]
        self.link = question["link"]

    def show(self):
        with st.container(border=True):
            st.text(self.question_text)
            st.divider()

            for i, option in enumerate(self.question_options):
                if self.given_answare is None:
                    st.markdown(f" - {option}")
                elif self.correct_answare == self.given_answare and i == self.correct_answare:
                    st.success(f" - {option}")
                elif i == self.correct_answare:
                    st.success(f" - {option} [CORRECT ANSWARE]")
                elif i == self.given_answare:
                    st.error(f" - {option} [YOUR ANSWARE]")
                else:
                    st.markdown(f" - {option}")

            st.divider()
            if self.link is not None:
                st.page_link(self.link, label=self.link, icon="🔗")


class Recap():

    def __init__(self):
        pass

    @classmethod
    def _charts(cls, exam_results):
        labels = 'Unanswared', 'Error', 'Correct'
        sizes = [exam_results["unanswared"], exam_results["error"],exam_results["correct"]]
        explode = (0, 0, 0.1)  # only "explode" the first slice
        colors = ["grey", "red", "green"]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90, colors=colors)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)

    @classmethod
    def homepage(cls):
        st.header(title_page_text, divider="blue")
        exam_results = st.session_state["exam_results"]
        questions_submitted = st.session_state["questions_submitted"]

        scores_text = f"## :green[CORRECT]: {exam_results["correct"]} - :red[ERROR]: {exam_results["error"]} - :grey[UNANSWARED]: {exam_results["unanswared"]}"
        st.markdown(scores_text)
        cls._charts(exam_results)

        for question in questions_submitted:
            QuestionCard(question).show()

        if st.button(quit_button_text, use_container_width=True, type="primary"):
            st.switch_page("pages/Home.py")


Recap.homepage()