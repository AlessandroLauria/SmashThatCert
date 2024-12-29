import sys
import requests
import os
from pathlib import Path
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
sys.path.append(str(Path(__file__).parent.parent))
from Libs.ConfigHandler import ConfigHandler
from Libs.MySql import Mysql

config_scraper = ConfigHandler(os.path.join(str(Path(__file__).parent),"Config"), "scraper")
config_database = ConfigHandler(os.path.join(str(Path(__file__).parent),"Config"), "database")

class ExamTopicExam:

    def __init__(self, search_sentence, sleep_time_between_pages=3):
        self.search_sentence = search_sentence
        self.sleep_time_between_pages = sleep_time_between_pages
        self.config = config_scraper

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)

        self.question_info_extractor = QuestionInfoExtractor(self.config.question_extractor_conf)

    def _get_first_url(self, search):
        url = 'https://www.google.com/search'

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
        }
        parameters = {'q': search}

        content = requests.get(url, headers=headers, params=parameters).text
        soup = BeautifulSoup(content, 'html.parser')

        search = soup.find(id='search')
        first_link = search.find('a')

        first_url = first_link['href']
        return first_url

    def print_question_info(self):
        self.driver.get(self._get_first_url(self.search_sentence))
        pprint(self.question_info_extractor.question_info(self.driver))

class IngestQuestions:

    def __init__(self, ingest_question_conf=None):
        if ingest_question_conf is None:
            self.ingest_question_conf = config_scraper.ingest_question_conf
        else:
            self.ingest_question_conf = ingest_question_conf
        self.mysql_conf = config_database.mysql_conf
        self.query_conf = config_database.query_conf
        self.question_info_extractor = QuestionInfoExtractor(config_scraper.question_extractor_conf)

        self.mysql = Mysql(self.ingest_question_conf["database"], self.mysql_conf['user'],
                           self.mysql_conf['password'], self.mysql_conf['host'])

        self.exam_name = self.ingest_question_conf['exam_name']

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)

    def _get_first_url(self, search, link_to_search_limit=3):
        url = self.ingest_question_conf['search_engine_url']

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
        }
        parameters = {'q': search}

        content = requests.get(url, headers=headers, params=parameters).text
        soup = BeautifulSoup(content, 'html.parser')

        search = soup.find(id='search')
        first_link = search.find('a')

        first_url = first_link['href']
        return first_url

    def create_exams_list_table(self):
        try:
            query = self.query_conf["create_exam_list_table"]
            query = query.format(dest_database=self.ingest_question_conf["database"],
                                 dest_table_name=self.ingest_question_conf["exam_list_table"],
                                 source_database=self.ingest_question_conf["database"],
                                 source_table_name=self.ingest_question_conf["question_table"],
                                 )
            print(">> Creating exams list table")
            print(query.strip().split(";"))
            self.mysql.execute_actions(query.split(";"))
        except Exception as e:
            print(f"[ERROR] in query '{query}'")
            print(e)

    def ingest_exam_questions(self):

        sentence = f"examtopic {self.exam_name}" + "question number {}"

        start_num = int(self.ingest_question_conf["first_question_number"])
        end_num = int(self.ingest_question_conf["last_question_number"])+1

        print(f"Search sentence {sentence}")
        for i in range(start_num, end_num):
            try:
                self.driver.get(self._get_first_url(sentence.format(i)))
                current_url = self.driver.current_url
            except Exception as e:
                print(f"[ERROR] in scraping link '{sentence.format(i)}'")
                print(e)

            query_template = 'query template not found'
            try:
                question_info = self.question_info_extractor.question_info(self.driver)

                query_template = self.query_conf['ingest_question_query']
                query_template = query_template.format(table_name=self.ingest_question_conf["question_table"],
                                                       exam_name=self.exam_name,
                                                       question_number=i,
                                                       question_text=question_info['question_text'].replace("'", "").replace('"', '').replace('\\', '/'),
                                                       question_options="$$$".join(question_info['question_options']).replace("'", "").replace('"', '').replace('\\', '/'),
                                                       most_voted=question_info['most_voted'],
                                                       link=current_url
                                                       )

                self.mysql.execute_actions([query_template])
                print(f"- Ingested question {i} of exam '{self.exam_name}'")
            except Exception as e:
                print(f"[ERROR] in query '{query_template}'")
                print(e)

        self.create_exams_list_table()

        self.mysql.close()
        print("DONE")



class QuestionInfoExtractor:

    def __init__(self, config):
        self.config = config

    def _find_text(self, driver, xpath):
        element = driver.find_element(By.XPATH, xpath)
        return element.text

    def _find_multiple_text(self, driver, xpath):
        options = driver.find_elements(By.XPATH, xpath)
        options_list = []
        for op in options:
            objects = op.find_elements(By.TAG_NAME, "li")
            for obj in objects:
                options_list.append(obj.text)

        return options_list

    def _find_most_voted(self, driver, button_xpath, answare_xpath):
        button = driver.find_element(By.XPATH, button_xpath)
        button.click()

        options = driver.find_elements(By.XPATH, answare_xpath)

        most_voted = "-1"
        for i,op in enumerate(options):
            objects = op.find_elements(By.TAG_NAME, "li")
            print("test")
            for obj in objects:
                print(obj.text)
                if 'most voted' in obj.text.lower():
                    print("found most voted")
                    most_voted = obj.text[0]

        return most_voted

    def question_info(self, driver):
        question_info = {
            "exam": self._find_text(driver, self.config['exam_title_xpath']),
            "question_number": -1, #int(self._find_text(driver, self.config['question_number_xpath']).split('\n')[0][-3:]),
            "question_text": self._find_text(driver, self.config['question_xpath']),
            "question_options": self._find_multiple_text(driver, self.config['options_xpath']),
            "most_voted": self._find_most_voted(driver, self.config['show_answare_btn_xpath'],
                                                self.config['options_xpath'])
        }
        #print(question_info)
        return question_info

#IngestQuestions().ingest_exam_questions()
#exam_topic_exam = ExamTopicExam("exam topic GCP Professional Cloud Developer question number 1")
#exam_topic_exam.print_question_info()