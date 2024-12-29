import sys
import requests
import os
import time
import argparse
from pathlib import Path
from pprint import pprint
from selenium.webdriver.common.by import By
sys.path.append(str(Path(__file__).parent.parent))
from Libs.ConfigHandler import ConfigHandler
from ExamTopics import IngestQuestions

delay_seconds = 5

config_scraper = ConfigHandler(os.path.join(str(Path(__file__).parent),"Config"), "scraper")

ingest_question_conf = config_scraper.ingest_question_conf
scraping_exam_list = config_scraper.exam_scraping_list

def ingest_exam(exam, from_=None, to_=None):
    if exam["scraper"] == "ExamTopics":
        IngestQuestions(exam).ingest_exam_questions(from_, to_)

def wait():
    print(f"Delay to avoid ban of {delay_seconds} seconds:")
    for i in range(0, delay_seconds):
        print("...", i)
        time.sleep(1)

def get_conf(exam_id):
    conf = {}
    for exam in scraping_exam_list:
        if str(exam["id"]) == str(exam_id):
            conf = exam

    return conf

def full_ingestion():
    for exam in scraping_exam_list:
        ingest_exam(exam)
        wait()

def ingest_single_exam(exam_name, from_=None, to_=None):
    if from_ is not None and to_ is not None:
        ingest_exam(exam_name, from_, to_)
    else:
        ingest_exam(exam_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', "--full", action='store_true',help='start a full ingestion of all exams')
    parser.add_argument("--exam_id", help='start a full ingestion of a single exam')
    parser.add_argument('--from_question', help='if set with --exam option, ingestion will start from this question number')
    parser.add_argument('--to_question', help='if set with --exam option, ingestion will end at this question number')

    args = parser.parse_args()
    full_ingestion = args.full
    exam_id = args.exam_id
    from_ = args.from_question
    to_ = int(args.to_question) + 1 if args.to_question is not None else None

    if full_ingestion:
        full_ingestion()
    elif exam_id is not None:
        exam_conf = get_conf(exam_id)
        ingest_single_exam(exam_conf, from_, to_)


