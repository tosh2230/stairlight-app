FROM python:3.8.12

COPY poetry.lock pyproject.toml ./
RUN apt-get dist-upgrade && \
    apt-get update && \
    apt-get install -y build-essential graphviz && \
    python -m pip install --upgrade pip poetry && \
    poetry install --no-dev

EXPOSE 8080
WORKDIR /app
CMD poetry run streamlit run app.py \
    --browser.serverAddress="0.0.0.0" \
    --server.port=${PORT} \
    --server.baseUrlPath="/lighthouse"
