from abc import ABC

from models.noticia import Noticia
from servicos.s_api.inoticia_api import INoticiaApi

class NoticiaAPI(INoticiaApi, ABC):

    def __init__(self):
        pass

    def salvar_dados(self, noticia: Noticia):
        pass

    def consultar_dados_id(self, id_noticia) -> Noticia:
        pass