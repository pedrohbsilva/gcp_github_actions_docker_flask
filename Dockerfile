FROM python:3.10
COPY . /src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.0

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock /app
COPY pyproject.toml /app

RUN poetry config virtualenvs.create false \
&& poetry install --no-interaction --no-ansi

COPY . .

CMD gunicorn --bind 0.0.0.0:5000 app:app
