#Grab the latest alpine image
FROM alpine:latest

# Install python and pip
RUN apk add --no-cache --update python3 py3-pip python3-dev bash g++ git

ADD ./webapp/requirements.txt /tmp/requirements.txt

RUN pip3 install git+https://github.com/jose-carmona/flask-assistant.git

# Install dependencies
RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Run the image as a non-root user
RUN adduser -D myuser

# Add our code
ADD ./webapp /opt/webapp/
RUN chown myuser:myuser /opt/webapp/

# Expose is NOT supported by Heroku
# EXPOSE 5000 		

WORKDIR /opt/webapp
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn --bind 0.0.0.0:$PORT wsgi 

