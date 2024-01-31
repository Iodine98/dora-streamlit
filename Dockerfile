## Pull builder image
FROM python:3.11.7 as builder

# Set working directory
WORKDIR /app

# Copy poetry.lock and pyproject.toml
COPY pyproject.toml /app/


# Set Poetry environment variables
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.5.0 \
    POETRY_CACHE_DIR="/tmp/poetry_cache"
ENV PATH="$PATH:$POETRY_HOME/bin"

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install necessary dependencies
RUN poetry config installer.max-workers 10
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install -vvv --no-root

## Runtime Image
FROM  python:3.11.7 as runtime

# Set working directory
WORKDIR /app

# Set virtual environment and Path
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy the virtual environment from the builder
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy current contents of folder to app directory
COPY . /app

# Enable port 8501
EXPOSE 8501

# Execute Streamlit server on starting container
ENTRYPOINT ["streamlit", "run", "st_app.py"]
