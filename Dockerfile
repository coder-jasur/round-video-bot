FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src

RUN uv sync --locked --no-install-project
RUN uv sync --locked

COPY . .

CMD ["python", "-m", "src.app.main"]

