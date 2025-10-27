import pytest
from src.core.api_client import ChuckNorrisAPIClient
from src.core.logger import LOGGER  # <--- CORREÇÃO: Importa o logger para o mock
from unittest.mock import Mock, patch
import requests

BASE_URL = "http://fake.api.com/jokes/"

# Fixture que fornece o cliente API para os testes
@pytest.fixture
def client():
    return ChuckNorrisAPIClient(BASE_URL)

def test_api_client_success(client, mocker):
    """Deve retornar o JSON quando a requisição for bem-sucedida (status 200)."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "test_id", "value": "test joke"}
    mock_response.raise_for_status.return_value = None # Simula sucesso

    # Mocks: Substitui requests.get pela nossa resposta simulada
    mocker.patch('requests.get', return_value=mock_response)

    result = client.get("random")
    
    assert result == {"id": "test_id", "value": "test joke"}

def test_api_client_http_error(client, mocker):
    """Deve retornar None e logar erro em caso de erro HTTP (ex: 404)."""
    mock_response = Mock()
    mock_response.status_code = 404
    
    # Faz raise_for_status simular um erro HTTP
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")

    # Mocks: Substitui requests.get
    mocker.patch('requests.get', return_value=mock_response)
    
    # Mocks: Espiona o LOGGER importado
    mock_logger = mocker.spy(LOGGER, 'error') # <--- CORREÇÃO: Usa a variável LOGGER importada

    result = client.get("nonexistent_endpoint")
    
    assert result is None
    # Verifica se o método de erro do logger foi chamado
    mock_logger.assert_called_once()
    assert "ERRO HTTP (404)" in mock_logger.call_args[0][0]

def test_api_client_connection_error(client, mocker):
    """Deve retornar None e logar erro em caso de erro de conexão/timeout."""
    # Mocks: Faz requests.get levantar um erro de conexão diretamente
    mocker.patch('requests.get', side_effect=requests.exceptions.ConnectionError("Timeout"))
    mock_logger = mocker.spy(LOGGER, 'error') # <--- CORREÇÃO: Usa a variável LOGGER importada

    result = client.get("random")
    
    assert result is None
    mock_logger.assert_called_once()
    assert "ERRO de Conexão ou Timeout" in mock_logger.call_args[0][0]