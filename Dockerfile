FROM python:3.10 as python-base

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.poetry/bin:$PATH"

RUN mkdir booking

WORKDIR /booking

COPY /pyproject.toml /booking 

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install 

COPY . .

RUN chmod a+x /booking/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]