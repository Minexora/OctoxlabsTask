FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirments.txt /code/
RUN pip install --no-cache-dir -r requirments.txt
COPY . /code/
