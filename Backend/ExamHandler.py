import sys
import os
import random
import streamlit as st
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from Libs.ConfigHandler import ConfigHandler
from Libs.MySql import Mysql

config_database = ConfigHandler(os.path.join(str(Path(__file__).parent.parent),"Scraper", "Config"), "database")

mapping_n2c = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
}

mapping_c2n = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
}

class ExamHandler():

    def __init__(self, exam_name, num_questions=-1, shuffle_questions=False):
        self.exam_name = exam_name
        self.num_questions = num_questions
        self.shuffle_questions = shuffle_questions

        self.mysql_conf = config_database.mysql_conf
        self.query_conf = config_database.query_conf

        self.exam_questions = []

        self.current_question_index = -1

        self._retrieve_questions()

    def _retrieve_questions(self):
        self.mysql = Mysql(self.mysql_conf["database"], st.secrets.db_credentials.username,
                           st.secrets.db_credentials.password, st.secrets.db_credentials.host,
                          st.secrets.db_credentials.port)

        query = self.query_conf["read_questions_query"]\
            .format(table_name=self.mysql_conf["question_table"], exam_name=self.exam_name)
        raw_questions = self.mysql.execute_query(query)

        all_questions = []

        for raw_quest in raw_questions:
            formatted_quest = {
                "exam_name": raw_quest[0],
                "question_number": raw_quest[1],
                "question_text": raw_quest[2],
                "question_options": raw_quest[3].split("$$$"),
                "most_voted": raw_quest[4],
                "link": raw_quest[5],
                "option_selected": None
            }
            all_questions.append(formatted_quest)

        if self.shuffle_questions:
            random.shuffle(all_questions)

        if self.num_questions != -1:
            n_quest = self.num_questions if self.num_questions <= len(all_questions) else len(all_questions)
            all_questions = all_questions[:n_quest]

        self.exam_questions = all_questions

        self.mysql.close()

    def next_question(self):
        if self.current_question_index + 1 >= len(self.exam_questions):
            return None #Reached the end

        self.current_question_index += 1
        return self.exam_questions[self.current_question_index]

    def previous_question(self):
        if self.current_question_index - 1 < 0:
            return None  # No previous questions

        self.current_question_index -= 1
        return self.exam_questions[self.current_question_index]

    def change_question(self, index=0):
        if (index - 1 < 0) or (index - 1 >= len(self.exam_questions)):
            return None

        self.current_question_index = index - 1
        return self.exam_questions[self.current_question_index]

    def set_option_selected(self, question_index, option_selected):
        self.exam_questions[question_index]["option_selected"] = option_selected

    def collect_results(self):
        correct = 0
        error = 0
        unanswared = 0
        for question in self.exam_questions:
            question["most_voted"] = mapping_c2n[question["most_voted"]]
            correct_answare = question["most_voted"]
            given_answare = question["option_selected"]

            if given_answare is None:
                unanswared += 1
            elif correct_answare != given_answare:
                error += 1
            else:
                correct +=1

        results = {"correct": correct, "error": error, "unanswared": unanswared}

        return results, self.exam_questions

    def get_current_question_info(self):
        return self.exam_questions[self.current_question_index]

    def get_total_num_questions(self):
        return len(self.exam_questions)

    def get_current_question_num(self):
        return self.current_question_index


class ExamMetadata():

    mysql_conf = config_database.mysql_conf
    query_conf = config_database.query_conf

    def __init__(self):
        pass

    @classmethod
    def _query_exams_list(cls):
        mysql = Mysql(cls.mysql_conf["database"], st.secrets.db_credentials.username,
                      st.secrets.db_credentials.password, st.secrets.db_credentials.host)

        query = cls.query_conf["get_exam_list_query"]\
                .format(database=cls.mysql_conf["database"],
                        table_name=cls.mysql_conf["exam_list_table"])

        exams_list = []
        try:
            exams_list = mysql.execute_query(query)
        except Exception as e:
            print(f"[ERROR] in query '{query}'")
            print(e)

        mysql.close()

        return exams_list

    @classmethod
    def get_exams_list(cls):
        exams_list = [f"{x[0]} - total questions: {x[1]} - last update: {x[2]}" for x in cls._query_exams_list()]
        return exams_list

    @classmethod
    def get_exams_last_updates(cls):
        result = {x[0]: x[2] for x in cls._query_exams_list()}
        return result


#ExamHandler("GCP Professional Cloud Developer")
#ExamMetadata().get_exams_list()
