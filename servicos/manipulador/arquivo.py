import os
from abc import ABC
from typing import Generic, TypeVar


class Arquivo(ABC):
    def __init__(self, nome_arquivo: str):
        self._caminho_raiz = os.getcwd()
        self._nome_arquivo = nome_arquivo

    @property
    def nome_arquivo(self):
        return self._nome_arquivo

    @nome_arquivo.setter
    def nome_arquivo(self, nome_arquivo):
        self._nome_arquivo = nome_arquivo