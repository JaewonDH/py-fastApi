FROM python:3.13

# Poetry 설치
RUN pip install -U poetry

WORKDIR /workdir

COPY poetry.lock pyproject.toml /workdir/
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction

COPY . /workdir

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]