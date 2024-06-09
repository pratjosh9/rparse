FROM python:3.12-slim-bookworm

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.7.1 \
  DJANGO_SETTINGS_MODULE="config.local_settings"

# Set up deps:
RUN apt-get update && apt-get -y install sudo pipx
RUN pipx ensurepath
# Install poetry
RUN pipx install poetry
# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Project initialization:
# RUN poetry export -f requirements.txt --output requirements.txt
# RUN pip3 install -r requirements.txt
RUN poetry install

COPY . /app/

EXPOSE 8000

# open localhost:8000 to view the UI
CMD ["poetry", "run", "python3", "./manage.py", "runserver", "0.0.0.0:8000"]