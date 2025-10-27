import requests
from typing import Optional, Any
from src.core.logger import LOGGER
from src.core.exceptions import NetworkError, APIProcessingError 

class ChuckNorrisAPIClient:
    """
    Cliente para interagir com a API de Chuck Norris.
    Lida com requisições HTTP e tratamento de erros de rede/API.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url
        LOGGER.info(f"API Client inicializado com URL: {base_url}")

    def get(self, endpoint: str, params: Optional[dict] = None) -> Optional[Any]:
        """
        Executa uma requisição GET para um endpoint específico.
        
        Levanta NetworkError em caso de falha de conexão/timeout.
        Levanta APIProcessingError em caso de erro HTTP (status != 2xx).
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            # 1. Checagem de Status HTTP (Erros 4xx, 5xx)
            response.raise_for_status()
            
            # 2. Se for sucesso (2xx), retorna o JSON
            return response.json()

        except requests.exceptions.HTTPError as e:
            # Captura erros de status HTTP (4xx, 5xx)
            status_code = e.response.status_code
            error_msg = f"ERRO HTTP ({status_code}) ao acessar o endpoint '{endpoint}'."
            
            LOGGER.error(error_msg)
            raise APIProcessingError(
                message=error_msg, 
                status_code=status_code, 
                endpoint=endpoint
            ) from e

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            # Captura erros de conexão/rede/timeout
            error_msg = f"ERRO de Conexão ou Timeout ao tentar acessar '{url}'."
            
            LOGGER.error(error_msg)
            raise NetworkError(
                message=error_msg,
                original_exception=e
            ) from e

        except Exception as e:
            # Captura erros inesperados (ex: JSONDecodeError se a API retornar HTML)
            error_msg = f"Erro inesperado ao processar a resposta da API: {type(e).__name__}"
            LOGGER.error(error_msg)
            raise APIProcessingError(
                message=error_msg,
                endpoint=endpoint
            ) from e