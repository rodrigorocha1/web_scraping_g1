from abc import abstractmethod, ABC


class WebScapingBase(ABC):

    @abstractmethod
    def conectar_site(self):
        pass

    @abstractmethod
    def obter_dados(self):
        pass
