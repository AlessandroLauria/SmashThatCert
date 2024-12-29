# SmashThatCert
![smash_that_cert_icon.png](images/smash_that_cert_icon.png)
## 1 Components

### 1.1 frontend
### 1.2 backend
### 1.3 scraper

## 2 How to run

To run che **webapp** you need to lauch this command by command line
```console
python -m streamlit run ./Frontend/main.py --client.showSidebarNavigation=False
```

To run a **full ingestion** of the questions, run this command
```console
python ./Scraper/ingest_questions.py
```

All the metadata about what exams to ingest in the database and the number of question for each exam is set in the **scraper_config.yaml** file