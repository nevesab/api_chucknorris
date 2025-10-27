import logging
from datetime import datetime
import os

def setup_logger(log_dir="logs"):
    """
    Configura e retorna o logger principal com saída para console e arquivo.
    O arquivo de log é organizado em uma estrutura de pastas: logs/ANO/MES/DIA/
    """
    logger = logging.getLogger('ChuckNorrisRPA')
    logger.setLevel(logging.INFO)

    # Verifica se já há handlers para evitar duplicação
    if logger.handlers:
        return logger

    # 1. Cria a estrutura dinâmica de diretório
    now = datetime.now()
    log_file_dir = os.path.join(log_dir, now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'))
    os.makedirs(log_file_dir, exist_ok=True)
    
    # Nome do arquivo de log: ano-mes-dia-hora-minuto.log
    log_file_name = now.strftime('%Y-%m-%d-%H-%M.log')
    log_file_path = os.path.join(log_file_dir, log_file_name)
    
    # Formato de Log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 2. Handler para o Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # 3. Handler para o Arquivo de Log
    fh = logging.FileHandler(log_file_path, encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    logger.info(f"Logger configurado. Log de sessão salvo em: {log_file_path}")
    return logger

LOGGER = setup_logger()