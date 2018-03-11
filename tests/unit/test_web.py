import pytest
from flask import url_for

from app import create_app, application


@pytest.fixture
def app():
    app = create_app()
    return app


def test_app(client):
    response = client.get(url_for('.index'))
    assert response.status_code == 200
    assert 'noAWS' in str(response.data)