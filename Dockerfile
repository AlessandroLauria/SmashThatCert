FROM python:3.9-slim
WORKDIR /SmashThatCert
COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
CMD [ "python", "-m","streamlit","run","./Frontend/main.py","--client.showSidebarNavigation=False"]