import sys
import requests
import os
from pathlib import Path
from pprint import pprint
from selenium.webdriver.common.by import By
sys.path.append(str(Path(__file__).parent.parent))
from Libs.ConfigHandler import ConfigHandler
from ExamTopics import IngestQuestions

config_scraper = ConfigHandler(os.path.join(str(Path(__file__).parent),"Config"), "scraper")

ingest_question_conf = config_scraper.ingest_question_conf
scraping_exam_list = config_scraper.exam_scraping_list

def full_ingestion():
    for exam in scraping_exam_list:
        if exam["scraper"] == "ExamTopics":
            IngestQuestions(exam).ingest_exam_questions()

full_ingestion()

