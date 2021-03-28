FROM python:3.9.2
WORKDIR /home/webchat 
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD FLASK_APP=server.py FLASK_ENV="Development" flask run
EXPOSE 5000
