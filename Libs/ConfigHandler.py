import yaml
import os


def _load_config(config_folder, conf_file_name):
    abs_dir = os.path.dirname(__file__)
    conf_path = os.path.join(*[abs_dir, config_folder, conf_file_name])
    with open(conf_path, 'r') as file:
        conf = yaml.safe_load(file)

    return conf


class ConfigHandler:
    def __init__(self, folder, config_type):
        if config_type == "scraper":
            self.scraper_conf = _load_config(folder, "scraper_config.yaml")
            self.question_extractor_conf = self.scraper_conf['question_info_extractor']
            self.ingest_question_conf = self.scraper_conf['ingest_questions']
            self.exam_scraping_list = self.scraper_conf['exam_scraping_list']
        elif config_type == "database":
            self.database_conf = _load_config(folder, "database_config.yaml")
            self.mysql_conf = self.database_conf['mysql']
            self.query_conf = self.database_conf['query']
