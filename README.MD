# Web client for manage ElasticMQ

### Getting started
[![Requirements Status](https://requires.io/github/ArtyomAnohin/ElasticmqUI/requirements.svg?branch=master)](https://requires.io/github/ArtyomAnohin/ElasticmqUI/requirements/?branch=master)
[![Build Status](https://travis-ci.org/ArtyomAnohin/ElasticmqUI.svg?branch=master)](https://travis-ci.org/ArtyomAnohin/ElasticmqUI)
[![codecov](https://codecov.io/gh/ArtyomAnohin/ElasticmqUI/branch/master/graph/badge.svg)](https://codecov.io/gh/ArtyomAnohin/ElasticmqUI)

Install docker and run:
```
docker-compose up
docker-compose stop
```
Otherwise, for the standalone web service:
```
pip install -r requirements.txt
python start.py
```
Visit [http://localhost:5000](http://localhost:5000)

### Testing
#### For the run test standalone:
```
py.test --cov=app
```

#### For travis CI

- build Docker file
- compose docker-compose-ci to deploy conatiners with ElasticMQ and ElasticUI
- execute python test 

<img width="1236" alt="main" src="https://user-images.githubusercontent.com/12786801/37246411-2cb87c16-24b1-11e8-9581-2b4e26cd9fef.png">
<br><br>
<img width="1234" alt="queue" src="https://user-images.githubusercontent.com/12786801/37246412-2f907c04-24b1-11e8-8d69-dcb4d74004cd.png">

<br><br>
v.0.1 Beta