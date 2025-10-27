# api_chucknorris — Automação Python: Extração e Organização de Piadas Chuck Norris via API

> Documentação técnica

---

## Visão Geral

**api_chucknorris** é uma automação desenvolvida em Python para realizar a extração de piadas do site [Chuck Norris API](https://api.chucknorris.io/), agrupadas por categoria.  
O sistema automatiza todo o fluxo — desde a coleta das categorias, obtenção das piadas, salvamento dos dados em planilha Excel, até a leitura e exibição estruturada dos resultados no console.

O projeto foi construído priorizando **clareza arquitetural**, **resiliência** (com tratamento de exceções diferenciado), **observabilidade** e **modularidade**, garantindo fácil manutenção e reuso.

---

## Recursos / Resultado esperado

Ao executar a automação, o usuário obtém:

* Uma planilha Excel (`data/chuck_jokes.xlsx`) contendo uma piada para cada categoria retornada pela API.  
  As colunas principais são: **id**, **url**, **value**, **category**.
* Impressão no console de todos os registros extraídos e lidos da planilha, em formato tabular.
* Logs detalhados de execução, com histórico diário organizado por data em `logs/YYYY/MM/DD/`.
* **Tratamento de Erros Explícito:** Em caso de falha (rede, API ou disco), o log exibe uma mensagem crítica detalhando a causa (ex: `NetworkError` ou `DataPersistenceError`).

---

## Principais decisões de arquitetura (resumo)

1. **Extração via API oficial (requests)**  
   * O projeto utiliza a API pública do [Chuck Norris API](https://api.chucknorris.io/) para obter dados estruturados de forma estável.  
   * Essa abordagem garante **confiabilidade** e **simplicidade**, evitando scraping manual de HTML ou parsing de conteúdo instável.

2. **Gerenciamento de Exceções Customizado** **(NOVO)**  
   * Foi definida uma hierarquia de exceções customizadas (`ChuckNorrisRPAError` base).  
   * Erros de rede (`NetworkError`), falhas da API (`APIProcessingError`) e problemas de I/O em disco (`DataPersistenceError`) são diferenciados, permitindo que a camada de negócio (collector) reaja de forma inteligente (ex: pular uma piada com erro, mas parar em erro de rede).

3. **Camadas funcionais separadas**  
   * `src/core` → componentes centrais (requisições HTTP, **tratamento de exceções**, manipulação de planilhas e logs).  
   * `src/process` → fluxos de negócio (extração e leitura).  
   * `src/utils` → suporte auxiliar, se necessário.  
   Essa separação facilita testes, depuração e futuras expansões (ex.: novas fontes de dados).

4. **Orquestração via `main.py`**  
   * O arquivo principal apenas coordena os módulos criados, mantendo o código limpo e fácil de entender.  
   * O fluxo principal está dividido em duas fases:  
     - **Fase 1:** Coleta de categorias e piadas, salvamento em planilha.  
     - **Fase 2:** Leitura e exibição dos dados salvos.

5. **Observabilidade e logs estruturados**  
   * O logger foi configurado para salvar os registros com data e hora detalhadas, permitindo auditoria e rastreabilidade completa da execução.  
   * Os logs são salvos em diretórios por ano/mês/dia, tornando o histórico organizado e acessível.

6. **Uso de `.env` para parametrização**  
   * As variáveis de ambiente (como caminhos, configurações ou endpoints) podem ser controladas via arquivo `.env`.  
   * Essa prática evita valores fixos dentro do código, facilitando portabilidade e segurança.

---

## Dependências e justificativas técnicas

> Cada biblioteca foi escolhida com base em maturidade, clareza e adequação ao propósito.

* **requests**  
  * Biblioteca padrão de mercado para requisições HTTP.  
  * Usada em conjunto com o tratamento de exceções customizado para mapear erros de rede e HTTP.

* **pandas**  
  * Utilizada para manipulação tabular e escrita/leitura de planilhas Excel.  
  * Oferece estrutura DataFrame altamente otimizada, facilitando operações de leitura, escrita e formatação.

* **openpyxl**  
  * Biblioteca oficial de manipulação de arquivos `.xlsx`.  
  * Usada pelo pandas para persistir os dados no formato Excel.  
  * Permite controle sobre planilhas, formatos e compatibilidade com versões modernas do Excel.

* **python-dotenv**  
  * Facilita a leitura de variáveis de ambiente a partir de um arquivo `.env`.  
  * Evita exposição de parâmetros diretamente no código-fonte e simplifica a configuração local.

* **logging (biblioteca padrão)**  
  * Implementa a rastreabilidade completa da execução.  
  * Configurado para salvar logs em arquivos datados e exibir mensagens claras no console.  
  * Fundamental para auditoria, depuração e manutenção.

* **tabulate (opcional)**  
  * Usada para imprimir tabelas de forma legível no console, simulando relatórios visuais.  
  * Melhora a experiência de leitura dos resultados sem depender de interfaces gráficas.

---

## Estrutura do projeto

```bash
api_chucknorris/
├── src/
│ ├── core/
│ │ ├── api_client.py
│ │ ├── logger.py
│ │ └── exceptions.py
| ├── data/
| | ├── sheet_handler.py 
│ ├── process/
│ │ ├── collector.py
│ └── /model
|   └── joke_model.py
├── data/               
├── logs/                  
├── .env.example
├── main.py
└── requirements.txt 
```

---

## Requisitos

> Python 3.8 ou superior  
> Conexão com a internet  

---

## Instalação

1. Clonar o repositório
```bash
# Clonar o repositório
git clone https://github.com/nnevesab/api_chucknorris.git
# Entrar na pasta do projeto
cd api_chucknorris
```

2. Criar ambiente virtual

```bash
python -m venv .venv
# ativa a venv
source .venv/bin/activate
# ou
.\.venv\Scripts\Activate.ps1
# ou
.\.venv\Scripts\activate.bat
# ou 
venv\Scripts\activate
```

3. Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Configurar variáveis de ambiente

Crie um .env na raiz do projeto (api_chucknorris/.env)

Copie e cole o conteúdo do .env.example

5. Executar

```bash
python main.py
```

---

## Próximos Passos e Planejamento de Evolução

1.  **Otimização de Performance:** Refatorar o módulo de coleta para utilizar a abordagem **assíncrona (ex: `asyncio` ou `concurrent.futures`)** na obtenção das piadas. Isso irá paralelizar as requisições HTTP, reduzindo significativamente o tempo total de execução.
2.  **Melhoria na Usabilidade (CLI):** Implementar uma **interface de linha de comando (CLI)** utilizando bibliotecas como `click` ou `argparse`. Isso permitirá a parametrização dinâmica de `--output-file`, `--log-level` e `--categories` sem modificar variáveis de ambiente, facilitando a operação e a integração em *pipelines*.
3.  **Redução de Custo e Robustez (Cache):** Introduzir uma camada de *caching* simples (ex: cache em memória ou disco) para a lista de categorias, minimizando requisições redundantes à API e aumentando a resiliência em caso de indisponibilidade temporária.