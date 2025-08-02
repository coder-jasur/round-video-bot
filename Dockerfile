FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY . /app

RUN apt update && apt install -y ffmpeg && apt clean && rm -rf /var/lib/apt/lists/*

RUN uv pip compile pyproject.toml > requirement.txt
RUN uv pip install -r requirement.txt --system

CMD ["python", "-m", "src.app.main"]

