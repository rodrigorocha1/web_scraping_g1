from typing import Optional, TypeVar
from abc import abstractmethod
import requests
from servicos.extracao.iwebscrapingbase import IWebScapingBase
from bs4 import BeautifulSoup
from tratamento.tratamento import Tratamento

U = TypeVar('U')


class WebScrapingBs4base(IWebScapingBase[BeautifulSoup, U]):

    def __init__(self, url: Optional[str], parse: str):
        """
        Construtor da classe
        :param url: url de conexão
        :type url: string
        :param parse: tipo de parse do bs4
        type parse: str
        """

        self._parse = parse
        self._url = url
        self._tratamento = Tratamento()

    @property
    def url(self) -> str:
        """
        Método de validação
        :return: url validada
        :rtype: str
        """
        if self._url is None:
            raise ValueError("URL não pode ser None")
        return self._url

    @url.setter
    def url(self, nova_url: str) -> None:
        """
        url do web scraping
        :param nova_url: url da extração
        :type nova_url: str
        :return:  Sem retorno
        :rtype: None
        """
        self._url = nova_url

    def abrir_conexao(self) -> BeautifulSoup:
        """
        Método para abrir a conexão do bs4
        :return: objeto do BeautifulSoup
        :rtype: BeautifulSoup
        """
        if self._url is None:
            raise ValueError("URL não pode ser None")
        response = requests.get(url=self._url)
        conteudo_response = response.content
        soup = BeautifulSoup(conteudo_response, self._parse)
        return soup

    @abstractmethod
    def obter_dados(self, dados: BeautifulSoup) -> U:
        """
        Método para obter os dados da extração
        :param dados: objeto BS4
        :type dados: BeautifulSoup
        :return: dados obtidos da Noticia
        :rtype: BeautifulSoup
        """
        pass
