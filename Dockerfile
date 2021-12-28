FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

WORKDIR /workspace
