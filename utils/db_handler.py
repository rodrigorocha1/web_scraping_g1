import logging
import sqlite3
from datetime import datetime
import os
from typing import Literal

LogLevel = Literal[0, 10, 20, 30, 40, 50]


class DBHandler(logging.Handler):
    def __init__(self, nome_pacote: str, formato_log: str, debug: LogLevel):
        super().__init__()
        self.__caminho_base = os.getcwd()
        self.__caminho_arquivo = os.path.join('sqlite:///', self.__caminho_base, 'logs.db')
        self.conn = sqlite3.connect('/home/rodrigo/Documentos/projetos/web_scraping_g1/logs.db')
        self.cursor = self.conn.cursor()
        self.loger = logging.getLogger(nome_pacote)
        self.__FORMATO_LOG = formato_log
        self.__formater = logging.Formatter(self.__FORMATO_LOG)
        self.setFormatter(self.__formater)
        self.loger.addHandler(self)
        self.loger.setLevel(debug)


    def emit(self, record):
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        status_code = getattr(record, 'status_code', None)
        log_entry = self.format(record)
        self.cursor.execute(
            'INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (timestamp, record.levelname, record.message, record.name, record.filename, record.funcName, record.lineno,
             status_code)
        )

        self.conn.commit()

    def close(self):
        self.conn.close()
        super().close()


if __name__ == '__main__':
    def teste():
        logger = logging.getLogger('meu_logger_db')
        logger.setLevel(logging.DEBUG)
