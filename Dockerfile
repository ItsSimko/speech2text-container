#Deriving the latest base image
FROM python:3.10

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/speech2text-container

#to COPY the remote file at working directory in container
COPY server.py ./

#to install the dependencies

RUN pip install -U openai-whisper

EXPOSE 8000

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.
CMD [ "python", "./server.py"]
