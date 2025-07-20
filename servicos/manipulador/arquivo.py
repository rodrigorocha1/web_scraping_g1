import os
from abc import ABC
from typing import Generic, TypeVar

from models.noticia import Noticia


class Arquivo(ABC):
    def __init__(self, nome_arquivo: str):
        self._caminho_raiz = os.getcwd()
        self._nome_arquivo = nome_arquivo
        self.__noticia = Noticia


    @property
    def nome_arquivo(self):
        return self._nome_arquivo

    @nome_arquivo.setter
    def nome_arquivo(self, nome_arquivo):
        self._nome_arquivo = nome_arquivo

    @property
    def noticia(self) -> Noticia:
        return self.__noticia

    @noticia.setter
    def noticia(self, nova_noticia: Noticia):
        if not isinstance(nova_noticia, Noticia) and nova_noticia is not None:
            raise TypeError("O atributo noticia deve ser uma instância de Noticia ou None")
        self.__noticia = nova_noticia