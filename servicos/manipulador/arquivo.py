import os
from abc import ABC, abstractmethod
from typing import Optional

from models.noticia import Noticia


class Arquivo(ABC):
    def __init__(self):
        self._caminho_raiz: str = os.getcwd()
        self._nome_arquivo: Optional[str] = None
        self._noticia: Optional[Noticia] = None

    @property
    def nome_arquivo(self) -> Optional[str]:
        return self._nome_arquivo

    @nome_arquivo.setter
    def nome_arquivo(self, nome_arquivo: str) -> None:
        self._nome_arquivo = nome_arquivo

    def __call__(self):
        self.reset()

    @property
    def noticia(self) -> Optional[Noticia]:
        return self.__noticia

    @noticia.setter
    def noticia(self, nova_noticia: Noticia) -> None:
        if not isinstance(nova_noticia, Noticia) and nova_noticia is not None:
            raise TypeError("O atributo noticia deve ser uma instância de Noticia ou None")
        self.__noticia = nova_noticia

    @abstractmethod
    def gerar_documento(self) -> None:
        pass

    def reset(self) -> None:
        self._caminho_raiz = os.getcwd()
        self._nome_arquivo = None
        self._noticia = None
