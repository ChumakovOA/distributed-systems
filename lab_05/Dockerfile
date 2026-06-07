FROM python:3.9-alpine

LABEL description="My Lab"
LABEL maintainer="Чумаков Олег"

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
