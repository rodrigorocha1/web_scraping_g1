import json

from config.config import Config
from models.noticia import Noticia
from servicos.s_api.inoticia_api import INoticiaApi
import requests


class NoticiaAPI(INoticiaApi):

    def __init__(self):
        self.__URL_API = Config.URL_API
        self.__USER_API = Config.USER_API
        self.__SENHA_API = Config.SENHA_API
        self.__ACCEPT = Config.CONTENT_TYPE
        self.__HEADER = {
            'accept': self.__ACCEPT
        }

    def checar_conexcao(self) -> bool:
        """
        Método para checar a conexão da API
        :return: Api sucesso ou falha
        :rtype: bool
        """
        url = self.__URL_API + '/health'
        response = requests.get(url, headers=self.__HEADER, timeout=10)
        if response.status_code == 200:
            return True
        return False

    def __realizar_login(self):
        url = self.__URL_API + '/login'
        payload = json.dumps(
            {
                "username": self.__USER_API,
                "senha": self.__SENHA_API
            }
        )
        response = requests.post(url=url, headers=self.__HEADER, timeout=10, data=payload)
        return response.json()['token']

    def salvar_dados(self, noticia: Noticia):
        """
        Método para salvar a noticia
        :param noticia: recebe a noticia
        :type noticia: Noticia
        """
        pass

    def consultar_dados_id(self, id_noticia) -> Noticia:
        """
        Método para consultar a no
        :param id_noticia:
        :type id_noticia:
        :return:
        :rtype:
        """
        pass


if __name__ == '__main__':
    noticia_api = NoticiaAPI()
    print(noticia_api.check_conexcao())
    a= noticia_api.realizar_login()
    print(a)