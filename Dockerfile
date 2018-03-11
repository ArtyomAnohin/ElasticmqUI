FROM python:3

EXPOSE 8080

COPY . /application
ADD ./ /application
VOLUME ["/application/config"]

WORKDIR /application
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["start.py"]