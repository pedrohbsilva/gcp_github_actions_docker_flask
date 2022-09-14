FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.0

# System deps:
RUN pip3 install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /src/app
COPY poetry.lock pyproject.toml /src/app

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . .

CMD poetry run flask run
