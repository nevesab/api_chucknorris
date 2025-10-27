from typing import List, Optional
from src.core.api_client import ChuckNorrisAPIClient
from src.core.logger import LOGGER
from src.model.joke_model import JokeModel, jokes_to_dict_list

CATEGORIES_ENDPOINT = "categories"
RANDOM_ENDPOINT = "random" 

class JokeCollector:
    """Orquestra a lógica de coleta de piadas da API Chuck Norris."""
    
    def __init__(self, client: ChuckNorrisAPIClient):
        self.client = client

    def get_all_categories(self) -> List[str]:
        """Busca a lista de categorias."""
        LOGGER.info("1.1 - Buscando lista de categorias...")
        data = self.client.get(CATEGORIES_ENDPOINT)
        
        if data and isinstance(data, list):
            LOGGER.info(f"1.2 - Encontradas {len(data)} categorias.")
            return data
        
        LOGGER.error("1.2 - Falha ao obter categorias da API. Retornando lista vazia.")
        return []

    def get_joke_for_category(self, category: str) -> Optional[JokeModel]:
        """Busca uma piada para uma categoria e a transforma no modelo JokeModel."""
        LOGGER.info(f"  -> Coletando piada para a categoria: '{category}'")
        
        params = {'category': category}
        data = self.client.get(RANDOM_ENDPOINT, params=params)
        
        if data:
            try:
                return JokeModel(
                    id=data.get("id", "N/A"),
                    url=data.get("url", "N/A"),
                    value=data.get("value", "N/A"),
                    category=category 
                )
            except Exception as e:
                LOGGER.error(f"Erro ao mapear dados da piada para '{category}': {e}")
                return None
        return None

    def collect_all_jokes_and_format(self) -> List[dict]:
        """Executa o processo principal de coleta e formatação."""
        
        categories = self.get_all_categories()
        if not categories:
            return []

        collected_jokes: List[JokeModel] = []
        
        for category in categories:
            joke = self.get_joke_for_category(category)
            if joke:
                collected_jokes.append(joke)

        LOGGER.info(f"1.3 - Coleta finalizada. {len(collected_jokes)} piadas coletadas.")

        return jokes_to_dict_list(collected_jokes)