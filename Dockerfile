#mcr.microsoft.com/playwright/python:v1.29.0-focal
# $ docker run --env-file ./my_env ubuntu bash
FROM mcr.microsoft.com/playwright/python:v1.29.0-focal

ADD main.py .

# Add python script to Docker
#COPY index.py /

#RUN pip install playwright python-dotenv
#COPY /app/main.py requirements.txt ./
COPY ./requirements.txt ./ 
RUN pip install  --no-cache-dir --upgrade -r /requirements.txt
RUN playwright install

CMD ["python", "./main.py"]