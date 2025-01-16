import sys
import os
import time
import argparse
from pathlib import Path
from datetime import date
sys.path.append(str(Path(__file__).parent.parent))
from Libs.ConfigHandler import ConfigHandler
from Backend.ExamHandler import ExamMetadata
from ExamTopics import IngestQuestions

delay_seconds = 5

config_scraper = ConfigHandler(os.path.join(str(Path(__file__).parent),"Config"), "scraper")

ingest_question_conf = config_scraper.ingest_question_conf
scraping_exam_list = config_scraper.exam_scraping_list

ExamMetadata.get_exams_list()

def ingest_exam(exam, from_=None, to_=None, check_delay=False):
    delay_days = exam["update_delay_days"]

    # checks if enough days passed to update the exam
    if check_delay:
        last_updates_dict = ExamMetadata.get_exams_last_updates()
        last_update_date = last_updates_dict[exam["exam_name"]]
        today_date = date.today()
        days_passed = (today_date - last_update_date).days
        print(f'Checking if exam {exam["exam_name"]} can be updated... today_date: {today_date} - last_update_date: {last_update_date} - days_passed: {days_passed} - delay_days: {delay_days}')

        if days_passed <= delay_days:
            print("> Exam scraping skipped cause not enough days passed")
            return

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
        ingest_exam(exam, check_delay=True)
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
    full_ing = args.full
    exam_id = args.exam_id
    from_ = args.from_question
    to_ = int(args.to_question) + 1 if args.to_question is not None else None

    if full_ing:
        full_ingestion()
    elif exam_id is not None:
        exam_conf = get_conf(exam_id)
        ingest_single_exam(exam_conf, from_, to_)


