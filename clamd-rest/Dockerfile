FROM python:2.7
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["sh", "start-server.sh"]
