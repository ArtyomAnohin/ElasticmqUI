import pytest
import time
from bs4 import BeautifulSoup
from flask import url_for
from app import create_app
import uuid


@pytest.fixture
def app():
    app = create_app()
    return app


QUEUE_NAME = 'first-queue'


def test_app(client):
    response = client.get(url_for('.index'))
    assert response.status_code == 200
    assert 'noAWS' in str(response.data)
    assert 'Error! Cannot connect to' not in str(response.data)
    response = client.get(url_for('.queue', name=QUEUE_NAME))
    assert response.status_code == 200


def test_delete_message(client):
    MESSAGE = str(uuid.uuid4())
    response = client.post(url_for('.add_message'), data={
        'queue_name': QUEUE_NAME,
        'message_body': MESSAGE
    })
    assert response.status_code == 302
    time.sleep(1)
    response = client.get(url_for('.queue', name=QUEUE_NAME))
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    message_id = soup.find("input", {"name": "message_id"}).attrs['value']
    time.sleep(1)
    response = client.post(url_for('.delete_message'), data={
        'queue_name': QUEUE_NAME,
        'message_id': message_id
    })
    assert response.status_code == 302
    time.sleep(1)
    response = client.get(url_for('.queue', name=QUEUE_NAME))
    assert MESSAGE not in str(response.data)


def test_purge_queue(client):
    MESSAGE = str(uuid.uuid4())
    response = client.post(url_for('.add_message'), data={
        'queue_name': QUEUE_NAME,
        'message_body': MESSAGE
    })
    assert response.status_code == 302
    time.sleep(1)
    response = client.get(url_for('.queue', name=QUEUE_NAME))
    assert response.status_code == 200
    assert MESSAGE in str(response.data)
    time.sleep(1)
    response = client.post(url_for('.purge_queue'), data={
        'queue_name': QUEUE_NAME
    })
    assert response.status_code == 200
    response = client.get(url_for('.queue', name=QUEUE_NAME))
    assert MESSAGE not in str(response.data)


def test_add_message(client):
    MESSAGE = str(uuid.uuid4())
    response = client.post(url_for('.add_message'), data={
        'queue_name': QUEUE_NAME,
        'message_body': MESSAGE
    })
    assert response.status_code == 302
    time.sleep(1)
    response = client.get(url_for('.queue', name=QUEUE_NAME))
    assert response.status_code == 200
    assert MESSAGE in str(response.data)


def test_404_page(client):
    response = client.get(url_for('.add_message'))
    assert response.status_code == 200
    assert 'I think you broke something ...' in str(response.data)
    response = client.get(url_for('.delete_message'))
    assert response.status_code == 200
    assert 'I think you broke something ...' in str(response.data)
    response = client.get(url_for('.purge_queue'))
    assert response.status_code == 200
    assert 'I think you broke something ...' in str(response.data)
