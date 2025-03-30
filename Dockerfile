FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Copy the project into the image
ADD . /chatbot

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /chatbot
RUN uv sync --frozen

EXPOSE 8081
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8081", "application:create_app()"] 