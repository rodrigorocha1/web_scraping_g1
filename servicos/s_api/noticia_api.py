from abc import ABC
from config.config import Config
from models.noticia import Noticia
from servicos.s_api.inoticia_api import INoticiaApi


class NoticiaAPI(INoticiaApi, ABC):

    def __init__(self):
        self.__url_api = Config.URL_API
        self.__user_api = Config.USER_API
        self.__senha_api = Config.SENHA_API

    def

    def salvar_dados(self, noticia: Noticia):
        pass

    def consultar_dados_id(self, id_noticia) -> Noticia:
        pass
