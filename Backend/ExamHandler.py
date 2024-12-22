import sys
import os
import random
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from Libs.ConfigHandler import ConfigHandler
from Libs.MySql import Mysql

config_database = ConfigHandler(os.path.join(str(Path(__file__).parent.parent),"Scraper", "Config"), "database")

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
        self.mysql = Mysql(self.mysql_conf["database"], self.mysql_conf['user'],
                           self.mysql_conf['password'], self.mysql_conf['host'])

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
                "option_selected": 0
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
            return None #Exam ended

        self.current_question_index += 1
        return self.exam_questions[self.current_question_index]

    def previous_question(self):
        if self.current_question_index - 1 < 0:
            return None  # No previous questions

        self.current_question_index -= 1
        return self.exam_questions[self.current_question_index]

    def get_total_num_questions(self):
        return len(self.exam_questions)

    def get_current_question_num(self):
        return self.current_question_index

#ExamHandler("GCP Professional Cloud Developer")