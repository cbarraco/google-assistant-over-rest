FROM python:3

EXPOSE 5000

WORKDIR /usr/src/app

COPY . .

RUN export CRYPTOGRAPHY_DONT_BUILD_RUST=1 && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py" ]