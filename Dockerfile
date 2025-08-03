FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /round-video-bot

COPY src/pyproject.toml /app/pyproject.toml
COPY . /app
RUN uv pip compile pyproject.toml > requirement.txt
RUN uv pip install -r requirement.txt --system --upgrade

CMD ["python", "-m", "src.app.main"]

