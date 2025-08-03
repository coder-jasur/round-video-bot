FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml /app/

RUN poetry export --without-hashes --format=requirements.txt -o requirement.txt

COPY . /app

RUN uv pip install -r requirement.txt --system --upgrade

CMD ["python", "-m", "src.app.main"]

