FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
COPY *.py /code/
RUN pip install -r requirements.txt
CMD ["python3", "/code/main.py"]


