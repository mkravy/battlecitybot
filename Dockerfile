FROM python:3.9-alpine
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt
COPY . /app
CMD ["python", "/app/battlecity/telegram.py"]