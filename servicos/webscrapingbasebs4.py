from typing import Generator
from abc import abstractmethod
import requests
from models.noticia import Noticia
from servicos.iwebscrapingbase import IWebScapingBase
from bs4 import BeautifulSoup
from tratamento.tratamento import Tratamento


class WebScrapingBs4base(IWebScapingBase[BeautifulSoup]):

    def __init__(self, url: str, parse: str):
        """
        Método para iniciar a classe com a url do g1
        Args:
            url (str): url do site rss
        """
        self._parse = parse
        self._url = url
        self._tratamento = Tratamento()

    def abrir_conexao(self) -> BeautifulSoup:
        """
            Método para abrir a conexão
        Returns:
            soup: objeto soup da página em xml

        """
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
              Noticia: Objetos do tipo Noticia gerados durante o processamento.


        """
        pass
