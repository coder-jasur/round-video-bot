FROM python:3.11-bullseye

WORKDIR /app

COPY . /app


RUN uv pip compile pyproject.toml > requirement.txt
RUN uv pip install -r requirement.txt --system

CMD ["python", "-m", "src.app.main"]

