# Start from Python 3.10 base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /code

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install Python dependencies
RUN poetry lock --no-update
RUN poetry install --no-root --no-dev

# Copy the application code into the container
COPY . .


# Set the default command to run the application
CMD ["poetry", "run", "python", "./app/main.py"]
