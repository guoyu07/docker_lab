FROM python:2.7
COPY ./requirements.txt /app/requirements.txt 
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . /app
CMD ["sh", "start-server.sh"]
#CMD ["python", "server.py"]
