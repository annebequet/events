FROM python:3.12-bookworm
EXPOSE 8000
WORKDIR /app 

# Installing build dependencies
RUN apt update && apt install build-essential -y


# Installing poetry
RUN pip install poetry

# Installing dependencies
COPY poetry.lock pyproject.toml /app/
RUN cd /app && poetry install

# installing code
COPY src/ /app 
# TODO use gunicorn as `runserver` is not secure
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
