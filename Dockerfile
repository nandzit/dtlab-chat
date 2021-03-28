FROM python:3.9.2
WORKDIR /home/webchat 
COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 
CMD FLASK_APP=server.py FLASK_ENV="Development" flask run
EXPOSE 5000
