FROM python:3.10.7-slim

COPY poetry.lock pyproject.toml ./
RUN apt-get dist-upgrade && \
    apt-get update && \
    apt-get install -y build-essential curl graphviz && \
    python -m pip install --upgrade pip && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH=${HOME}/.local/bin:${PATH} && \
    poetry config virtualenvs.create false && \
    poetry install --only main

EXPOSE 8080
COPY .streamlit/config.toml ${HOME}/.streamlit/
WORKDIR /app
COPY src/app.py src/mapping.yaml src/stairlight.yaml ./
CMD streamlit run app.py \
    --browser.serverAddress="0.0.0.0" \
    --server.port=${PORT} \
    --server.baseUrlPath=""
