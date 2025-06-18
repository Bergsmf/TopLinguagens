import json
from unittest.mock import MagicMock, patch

import pytest

from toplinguagens.classes.vagas import Vagas


@pytest.fixture
def mock_response():
    return {
        'jobs': [
            {
                'id': 1,
                'url': 'https://example.com/job_abc',
                'title': 'Software Engineer',
                'company_name': 'ABCT1',
                'company_logo': 'https://example.com/logo_abc',
                'category': 'Software Development',
                'tags': ['c#', 'react'],
                'job_type': 'contract',
                'publication_date': '2025-06-16T18:50:22',
                'candidate_required_location': 'Europe, UK, Asia',
                'salary': 'day rate or month rate based on experience',
                'description': 'XPTO abc',
            },
            {
                'id': 2,
                'url': 'https://example.com/job_def',
                'title': 'Environment Artist',
                'company_name': 'DEFT2',
                'company_logo': 'https://example.com/logo_def',
                'category': 'Design',
                'tags': ['video', 'editing'],
                'job_type': 'freelance',
                'publication_date': '2025-06-16T18:50:22',
                'candidate_required_location': 'Americas, LATAM',
                'salary': '',
                'description': 'XPTO def',
            },
            {
                'id': 3,
                'url': 'https://example.com/job_ghi',
                'title': 'Account Executive',
                'company_name': 'GHIT3',
                'company_logo': 'https://example.com/logo_ghi',
                'category': 'Sales / Business',
                'tags': [
                    'business development',
                    'account management',
                    'sales management',
                ],
                'job_type': 'full_time',
                'publication_date': '2025-06-16T18:50:22',
                'candidate_required_location': 'Brazil',
                'salary': '',
                'description': 'XPTO ghi',
            },
        ]
    }


@patch('toplinguagens.classes.vagas.requests.get')
@patch('toplinguagens.classes.vagas.os.getenv')
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
