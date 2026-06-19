FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install .

CMD ["python", "main.py"]