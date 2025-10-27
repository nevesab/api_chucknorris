from src.model.joke_model import JokeModel, jokes_to_dict_list

def test_joke_model_creation():
    """Deve criar uma instância de JokeModel com os atributos corretos."""
    joke = JokeModel(
        id="abc123xyz",
        url="http://example.com/joke",
        value="Chuck Norris can divide by zero.",
        category="dev"
    )
    assert joke.id == "abc123xyz"
    assert joke.category == "dev"
    assert "divide by zero" in joke.value

def test_joke_model_to_dict():
    """Deve converter a instância de JokeModel para um dicionário correto."""
    joke = JokeModel(
        id="abc123xyz",
        url="http://example.com/joke",
        value="Chuck Norris can divide by zero.",
        category="dev"
    )
    joke_dict = joke.to_dict()
    
    assert isinstance(joke_dict, dict)
    assert joke_dict["id"] == "abc123xyz"
    assert list(joke_dict.keys()) == ["id", "url", "value", "category"]

def test_jokes_to_dict_list():
    """Deve converter uma lista de JokeModel em uma lista de dicionários."""
    joke1 = JokeModel(id="1", url="u1", value="v1", category="c1")
    joke2 = JokeModel(id="2", url="u2", value="v2", category="c2")
    
    jokes_list = [joke1, joke2]
    dict_list = jokes_to_dict_list(jokes_list)
    
    assert isinstance(dict_list, list)
    assert len(dict_list) == 2
    assert dict_list[0]["category"] == "c1"