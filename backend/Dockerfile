FROM python:3.10-bullseye AS poetry
ENV PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$VENV_PATH/bin:$PATH"
RUN pip install poetry

FROM poetry AS dependencies
WORKDIR $PYSETUP_PATH
COPY pyproject.toml poetry.* $PYSETUP_PATH
RUN poetry install --no-dev

FROM dependencies AS development
WORKDIR /app
COPY . /app
EXPOSE 80
CMD uvicorn app.main:app --host 0.0.0.0 --port 80
