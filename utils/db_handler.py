import logging
import sqlite3
from datetime import datetime


class DBHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('/home/rodrigo/Documentos/projetos/web_scraping_g1/logs.db')
        self.cursor = self.conn.cursor()

    def emit(self, record):
        # Obtém timestamp formatado (yyyy-mm-dd hh:mm:ss)
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

        log_entry = self.format(record)
        print(log_entry)
        self.cursor.execute(
            'INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (timestamp, record.levelname, record.message, record.name, record.filename, record.funcName, record.lineno, status_code)
        )

        self.conn.commit()

    def close(self):
        self.conn.close()
        super().close()


if __name__ == '__main__':
    def teste():
        logger = logging.getLogger('meu_logger_db')
        logger.setLevel(logging.DEBUG)

        db_handler = DBHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        db_handler.setFormatter(formatter)

        logger.addHandler(db_handler)

        # Testes
        logger.info("Teste de log no banco!")
        logger.error("Erro gravado no banco!")
    teste()
