from typing import Generator, Optional
from abc import abstractmethod
import requests
from models.noticia import Noticia
from servicos.iwebscrapingbase import IWebScapingBase
from bs4 import BeautifulSoup
from tratamento.tratamento import Tratamento


class WebScrapingBs4base(IWebScapingBase[BeautifulSoup]):

    def __init__(self, url: Optional[str], parse: str):
        """
        Método para iniciar a classe com a url do g1
        Args:
            url (str): url do site rss
        """
        self._parse = parse
        self._url = url
        self._tratamento = Tratamento()

    @property
    def url(self) -> str:
        if self._url is None:
            raise ValueError("URL não pode ser None")
        return self._url

    @url.setter
    def url(self, nova_url: str) -> None:
        self._url = nova_url

    def abrir_conexao(self) -> BeautifulSoup:
        """
            Método para abrir a conexão

        Returns:    
            BeautifulSoup: objeto soup da página em xml
        """
        if self._url is None:
            raise ValueError("URL não pode ser None")
        response = requests.get(url=self._url)
        conteudo_response = response.content
        soup = BeautifulSoup(conteudo_response, self._parse)
        return soup

    @abstractmethod
    def obter_dados(self, dados: BeautifulSoup) -> Generator[Noticia, None, None]:
        """
          Obtém dados processados a partir da entrada fornecida.

          Args:
              dados (T): Dados de entrada para o processamento.


          Yields:
              Generator[Noticia, None, None] : Gerador com as noticias


        """
        pass
