from dataclasses import dataclass, asdict
from typing import List

@dataclass
class JokeModel: 
    """Modelo de dados para uma piada do Chuck Norris, focado nos campos requeridos."""
    id: str
    url: str
    value: str
    category: str
    
    def to_dict(self) -> dict:
        """Converte a dataclass para um dicionário padrão."""
        return asdict(self)
        
def jokes_to_dict_list(jokes: List[JokeModel]) -> List[dict]:
    """Converte uma lista de objetos JokeModel para uma lista de dicionários."""
    return [joke.to_dict() for joke in jokes]