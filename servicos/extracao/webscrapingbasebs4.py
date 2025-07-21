import logging
from typing import Optional, TypeVar
from abc import abstractmethod
import requests
from servicos.extracao.iwebscrapingbase import IWebScapingBase
from bs4 import BeautifulSoup
from tratamento.tratamento import Tratamento
from requests.exceptions import HTTPError, ConnectionError, ConnectTimeout, ReadTimeout, TooManyRedirects, \
    RequestException
from utils.log_pipeline import logger

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
        try:
            if self._url is None:
                raise ValueError("URL não pode ser None")
            logger.info(f'Conectando na URL {self._url}')
            response = requests.get(url=self._url)
            response.raise_for_status()
            conteudo_response = response.content
            logger.info('Sucesso ao conectar na url')
            try:
                soup = BeautifulSoup(conteudo_response, self._parse)
                return soup

            except Exception as e:
                logger.error(f'Erro inesperado {e}')

        except HTTPError as http_err:
            logger.error(f"Erro HTTP ({response.status_code}): {http_err} - Pipeline fechado")
            exit()
        except ConnectionError:
            logger.error(f'Erro de conexão na url {self._url} - Pipeline fechado')
            exit()
        except ConnectTimeout:
            logger.error(f'Tempo de conexão excedido url {self._url} - Pipeline fechado ')
            exit()
        except ReadTimeout:
            logging.error(f"Tempo de leitura excedido url {self._url} - Pipeline fechado")
            exit()
        except TooManyRedirects:
            logging.error("Redirecionamentos em excesso detectados. url {self._url} - Pipeline fechado")
        except RequestException as req_err:
            logging.error(f"Erro de requisição: {req_err} url {self._url} - Pipeline fechado")
        except Exception as e:
            logging.error(f"Erro inesperado: {e} url {self._url} - Pipeline fechado")


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
