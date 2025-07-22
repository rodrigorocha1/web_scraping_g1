from abc import abstractmethod, ABC
from models.noticia import Noticia


class INoticiaApi(ABC):

    @abstractmethod
    def checar_conexao(self) -> bool:
        pass

    @abstractmethod
    def salvar_dados(self, noticia: Noticia):
        pass

    @abstractmethod
    def consultar_dados_id(self, id_noticia) -> Noticia| str:
        pass

    def realizar_login(self):
        raise NotImplementedError
