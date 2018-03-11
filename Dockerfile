FROM       ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
EXPOSE 8080

COPY . /application
ADD ./config /application
VOLUME ["/application/config"]

WORKDIR /application
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["start.py"]