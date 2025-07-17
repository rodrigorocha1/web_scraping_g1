from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Generator
from models.noticia import Noticia

T = TypeVar('T')


class IWebScapingBase(ABC, Generic[T]):

    @property
    @abstractmethod
    def url(self) -> str:
        """
        Propriedade que retorna a URL atual.
        """
        pass

    @url.setter
    @abstractmethod
    def url(self, url: str) -> None:
        """
        Define a URL para conexão.
        """
        pass

    @abstractmethod
    def abrir_conexao(self) -> T:
        """
        Método para abrir a conexão

        Returns:
            A conexão com o site

        """
        pass

    @abstractmethod
    def obter_dados(self, dados: T) -> Generator[Noticia, None, None]:
        """
        Obtém dados processados a partir da entrada fornecida.

        Args:
            dados (T): Dados de entrada para o processamento.


        Yields:
            Generator[Noticia, None, None: Objetos do tipo Noticia gerados durante o processamento.


        """
        pass
