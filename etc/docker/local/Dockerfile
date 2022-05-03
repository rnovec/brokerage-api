FROM python:3.8-alpine

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY ./app/ /usr/src/app/
COPY ./etc/pip/ /usr/src/pip/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r pip/requirements-dev.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]