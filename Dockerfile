# Pull Python 3.11.7 base image
FROM python:3.11.7

# Set working directory
WORKDIR /app

# Copy current contents of folder to app directory
COPY . /app

# Set Poetry environment variables
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.5.0
ENV PATH="$PATH:$POETRY_HOME/bin"

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install necessary dependencies
RUN poetry config installer.max-workers 10
RUN poetry update -vv

# Enable port 8501
EXPOSE 8501

# Execute Streamlit server on starting container
CMD ["poetry", "run", "streamlit", "run", "st_app.py"]
