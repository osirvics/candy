FROM mcr.microsoft.com/playwright/python:v1.29.0-focal

ADD main.py .

COPY ./requirements.txt ./ 
RUN pip install  --no-cache-dir --upgrade -r /requirements.txt
RUN playwright install

CMD ["python", "./main.py"]