from servicos.manipulador.arquivo import Arquivo
from models.noticia import Noticia


class ArquivoDOCX(Arquivo):
    def __init__(self, nome_arquivo: str, noticia: Noticia):
        super().__init__(nome_arquivo=nome_arquivo)
        self.__noticia = Noticia
