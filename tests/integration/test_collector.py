import pytest
from src.process.collector import JokeCollector
# Importa o cliente da API, mesmo que seja mockado, para a tipagem
from src.core.api_client import ChuckNorrisAPIClient 
from src.model.joke_model import JokeModel
from unittest.mock import Mock, patch, call

# Dados de simulação
MOCK_CATEGORIES = ["dev", "food", "sport"]
MOCK_JOKE_DATA = {
    "dev": {"id": "id1", "url": "u1", "value": "Dev Joke", "categories": ["dev"]},
    "food": {"id": "id2", "url": "u2", "value": "Food Joke", "categories": ["food"]},
    "sport": {"id": "id3", "url": "u3", "value": "Sport Joke", "categories": ["sport"]},
}

@pytest.fixture
def mock_api_client(mocker):
    """Fixture que retorna um mock do cliente API."""
    mock_client = mocker.Mock(spec=ChuckNorrisAPIClient)
    
    # Configura o mock para responder às categorias e piadas
    mock_client.get.side_effect = lambda endpoint, params=None: (
        MOCK_CATEGORIES if endpoint == "categories" else MOCK_JOKE_DATA.get(params.get('category'))
    )
    return mock_client

@pytest.fixture
def collector(mock_api_client):
    """Fixture que retorna o JokeCollector com o cliente mockado."""
    return JokeCollector(mock_api_client)

def test_get_all_categories_success(collector, mock_api_client):
    """Deve retornar a lista de categorias simuladas e ser chamado corretamente."""
    categories = collector.get_all_categories()
    
    assert categories == MOCK_CATEGORIES
    # CORREÇÃO 1: O código de produção chama get(CATEGORIES_ENDPOINT) sem o segundo argumento.
    mock_api_client.get.assert_called_with("categories") 

def test_get_joke_for_category_success(collector, mock_api_client):
    """Deve buscar uma piada e mapeá-la corretamente para JokeModel."""
    joke_model = collector.get_joke_for_category("dev")
    
    assert isinstance(joke_model, JokeModel)
    assert joke_model.id == "id1"
    assert joke_model.category == "dev"
    # CORREÇÃO 2: A chamada usa um argumento posicional ('random') e um nomeado (params={'category': 'dev'}).
    mock_api_client.get.assert_called_with("random", params={'category': 'dev'}) 

def test_collect_all_jokes_and_format_full_success(collector, mock_api_client):
    """Deve orquestrar a coleta de piadas para todas as categorias e retornar a lista de dicts."""
    
    result_list = collector.collect_all_jokes_and_format()
    
    assert isinstance(result_list, list)
    assert len(result_list) == len(MOCK_CATEGORIES)
    
    dev_joke = next(item for item in result_list if item["category"] == "dev")
    assert dev_joke["value"] == "Dev Joke"
    
    # O mock_api_client.get é chamado 4 vezes. Assert_has_calls verifica a sequência.
    expected_calls = [
        call("categories"), # 1. Coletar categorias
        call("random", params={'category': 'dev'}),    # 2. Coletar dev
        call("random", params={'category': 'food'}),   # 3. Coletar food
        call("random", params={'category': 'sport'}),  # 4. Coletar sport
    ]
    mock_api_client.get.assert_has_calls(expected_calls, any_order=False)


def test_collect_all_jokes_and_format_partial_failure(collector, mocker):
    """Deve ignorar categorias que falham na chamada de piada e continuar."""
    
    # Configura um cliente mock customizado para simular falha em 'sport'
    mock_client_failure = mocker.Mock(spec=ChuckNorrisAPIClient)
    
    def side_effect_func(endpoint, params=None):
        if endpoint == "categories":
            return MOCK_CATEGORIES
        
        category = params.get('category')
        if category == "sport":
            return None # Simula falha/erro na API para 'sport'
        
        return MOCK_JOKE_DATA.get(category)
        
    mock_client_failure.get.side_effect = side_effect_func
    
    collector_partial = JokeCollector(mock_client_failure)
    result_list = collector_partial.collect_all_jokes_and_format()
    
    assert len(result_list) == 2 # Apenas 'dev' e 'food' devem ter sido coletados
    assert all(item["category"] != "sport" for item in result_list)