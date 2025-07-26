from abc import ABC, abstractmethod
from typing import Optional
from context.pipeline_context import PipelineContext
from utils.db_handler import DBHandler
import logging

FORMATO = '%(asctime)s %(filename)s %(funcName)s'
db_handler = DBHandler(nome_pacote='Handler', formato_log=FORMATO, debug=logging.DEBUG)

logger = db_handler.loger


class Handler(ABC):

    def __init__(self) -> None:
        self._next_handler: Optional['Handler'] = None

    def set_next(self, hander: "Handler") -> "Handler":
        self._next_handler = hander
        return hander

    def handle(self, context: PipelineContext) -> None:
        logger.info(f'{self.__class__.__name__} -> Iniciando web scraping')
        if self.executar_processo(context):
            logger.info(f'{self.__class__.__name__} -> Sucesso ao executar')
            if self._next_handler:
                self._next_handler.handle(context)
            else:
                logger.info(f'{self.__class__.__name__} ->  Último handler da cadeia')
        else:
            logger.warning(f'{self.__class__.__name__} -> Falha, pipeline interrompido')

    @abstractmethod
    def executar_processo(self, context: PipelineContext) -> bool:
        pass
