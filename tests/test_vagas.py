import json
from unittest.mock import MagicMock, patch

import pytest

from app.classes.vagas import Vagas


@pytest.fixture
def mock_response():
    return {
        'jobs': [
            {'id': 1, 'title': 'Dev Python'},
            {'id': 2, 'title': 'Data Scientist'},
        ]
    }


@patch('app.classes.vagas.requests.get')
@patch('app.classes.vagas.os.getenv')
def test_obtem_dump_vagas(mock_getenv, mock_get, tmp_path, mock_response):
    # Arrange
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = mock_response
    mock_get.return_value = mock_resp
    vagas = Vagas()
    vagas.path_file = tmp_path / 'vagas.json'

    # Act
    vagas.obtem_vagas()
    vagas.dump_vagas()

    # Arrange
    assert vagas.vagas == mock_response['jobs']
    with open(vagas.path_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data == mock_response['jobs']
