import os
from dotenv import load_dotenv
from src.core.api_client import ChuckNorrisAPIClient
from src.process.collector import JokeCollector
from src.data.sheet_handler import save_to_excel, read_and_display
from src.core.logger import LOGGER 
from src.core.exceptions import ChuckNorrisRPAError

def main():

    load_dotenv()
    
    # Parâmetros
    API_URL = os.getenv("CHUCK_NORRIS_API_URL")
    OUTPUT_FILE = "data/chuck_jokes.xlsx"

    LOGGER.info("="*60)
    LOGGER.info("INICIANDO EXTRAÇÃO DE PIADAS CHUCK NORRIS")
    LOGGER.info("="*60)
    
    try:
        # Inicialização dos componentes
        api_client = ChuckNorrisAPIClient(API_URL)
        collector = JokeCollector(api_client)

        # --- FASE 1: EXTRAÇÃO DA API E SALVAMENTO ---
        LOGGER.info("--- INÍCIO DA FASE 1: EXTRAÇÃO DA API E SALVAMENTO ---")
        LOGGER.info("1.1 - Buscando lista de categorias...")
        
        # Coleta os dados (a exceção será lançada se o erro for crítico)
        collected_data = collector.collect_all_jokes_and_format()
        
        LOGGER.info(f"1.3 - Coleta finalizada. {len(collected_data)} piadas coletadas.")

        # Garante o diretório de saída
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        # Salva em disco (lança DataPersistenceError em caso de falha)
        save_to_excel(collected_data, OUTPUT_FILE)
        
        LOGGER.info("--- FIM DA FASE 1 ---")

        # --- FASE 2: LEITURA E APRESENTAÇÃO ---
        LOGGER.info("\n--- INÍCIO DA FASE 2: LEITURA E APRESENTAÇÃO ---")
        
        # Lê o arquivo e exibe no console (lança DataPersistenceError em caso de falha)
        read_and_display(OUTPUT_FILE)
        
        LOGGER.info("--- FIM DA FASE 2 ---")
        
    except ChuckNorrisRPAError as e:
        # Captura QUALQUER erro customizado do RPA (Rede, API ou Disco)
        LOGGER.critical(f"AUTOMAÇÃO FALHOU: Erro específico detectado: {e.__class__.__name__}. Mensagem: {e}")
        
    except Exception as e:
        # Captura erros inesperados que não foram tratados nas camadas inferiores
        LOGGER.critical(f"AUTOMAÇÃO FALHOU: Erro GENÉRICO inesperado: {e.__class__.__name__}. Detalhes: {e}")

    finally:
        LOGGER.info("="*60)
        LOGGER.info("CONCLUÍDO")
        LOGGER.info("="*60)

if __name__ == "__main__":
    main()