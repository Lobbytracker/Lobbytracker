FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /src

# Install the application dependencies.
WORKDIR /src
RUN uv sync --frozen --no-cache

# Run the application.
CMD [".venv/bin/fastapi", "run", "src/main.py", "--port", "8000", "--host", "0.0.0.0"]
