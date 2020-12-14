FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

ENV FLASK_APP=/usr/src/app/main.py
CMD [ "python", "-m", "flask", "run" ]