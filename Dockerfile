FROM python:3.7

WORKDIR project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN mkdir models

CMD ["bash","/project/config/entrypoint.sh"]