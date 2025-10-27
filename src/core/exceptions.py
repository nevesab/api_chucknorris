class ChuckNorrisRPAError(Exception):
    """Exceção base para todos os erros customizados do RPA."""
    pass

class NetworkError(ChuckNorrisRPAError):
    """Erro de Rede (Timeout, ConnectionError, DNS, etc.)."""
    def __init__(self, message="Falha de conexão com a API ou Timeout.", original_exception=None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)

class APIProcessingError(ChuckNorrisRPAError):
    """Erro na API (Status HTTP != 200 ou estrutura de resposta inválida)."""
    def __init__(self, message="Erro de processamento da API.", status_code=None, endpoint=None):
        self.message = message
        self.status_code = status_code
        self.endpoint = endpoint
        detail = f"Status {status_code}" if status_code else "Estrutura inválida"
        full_msg = f"{self.message} [Detalhe: {detail}]"
        super().__init__(full_msg)

class DataPersistenceError(ChuckNorrisRPAError):
    """Erro de I/O ao salvar ou ler o arquivo (Disco, Permissão, Formato)."""
    def __init__(self, filename, action="salvar/ler", original_exception=None):
        self.message = f"ERRO de I/O. Falha ao {action} o arquivo: {filename}"
        self.original_exception = original_exception
        super().__init__(self.message)