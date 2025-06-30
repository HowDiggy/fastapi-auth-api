# 1. Use an official python runtime as a parent image
FROM python:3.13-slim

# 2. set the working directory inside the container
WORKDIR /code

# 3. copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. copy the rest of the application code into the working directory
COPY ./app /code/app

# 5. the command that will be run when the container starts
#   --host 0.0.0.0 makes the server accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]