FROM python:3.8.12

COPY poetry.lock pyproject.toml ./
RUN apt-get dist-upgrade && \
    apt-get update && \
    apt-get install -y build-essential graphviz && \
    python -m pip install --upgrade pip && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - && \
    export PATH=${HOME}/.poetry/bin:${PATH} && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

EXPOSE 8080
COPY .streamlit/config.toml /root/.streamlit/
WORKDIR /app
COPY src/app.py src/mapping_sample.yaml src/stairlight.yaml ./
CMD streamlit run app.py \
    --browser.serverAddress="0.0.0.0" \
    --server.port=${PORT} \
    --server.baseUrlPath=""
