
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s -  %(levelname)s -  %(message)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

#  %(asctime)s -  %(levelname)s -  %(message)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d

# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG
# NOTSET


# Especificador	Descrição	Exemplo de saída
# %(asctime)s	Data e hora do evento de log	2025-07-20 19:30:00,123
# %(levelname)s	Nível do log (DEBUG, INFO, WARNING, ERROR, CRITICAL)	DEBUG
# %(message)s	Mensagem do log	This message should appear
# %(name)s	Nome do logger (geralmente o módulo)	root
# %(filename)s	Nome do arquivo de onde veio o log	app.py
# %(funcName)s	Nome da função que chamou o log	minha_funcao
# %(lineno)d	Número da linha no arquivo onde o log foi chamado	27
# %(threadName)s	Nome da thread que gerou o log	MainThread
# %(process)d	PID do processo que gerou o log	12345


# import logging
# import sqlite3
#
# class DBHandler(logging.Handler):
#     def __init__(self, db_path='logs.db'):
#         super().__init__()
#         self.conn = sqlite3.connect(db_path)
#         self.cursor = self.conn.cursor()
#         self._create_table()
#
#     def _create_table(self):
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS logs (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 level TEXT,
#                 message TEXT,
#                 created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         ''')
#         self.conn.commit()
#
#     def emit(self, record):
#         log_entry = self.format(record)
#         self.cursor.execute(
#             'INSERT INTO logs (level, message) VALUES (?, ?)',
#             (record.levelname, log_entry)
#         )
#         self.conn.commit()
#
#     def close(self):
#         self.conn.close()
#         super().close()
#
#
# # Configurando o logger com o handler do banco
# logger = logging.getLogger('meu_logger_db')
# logger.setLevel(logging.DEBUG)
#
# db_handler = DBHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
# db_handler.setFormatter(formatter)
#
# logger.addHandler(db_handler)
#
# # Usando o logger normalmente
# logger.info("Teste de log no banco!")
# logger.error("Erro gravado no banco!")
