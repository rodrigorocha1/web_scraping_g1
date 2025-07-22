class Variaveis:
    _instancia = None
    _variaveis = {}

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super(Variaveis, cls).__new__(cls)
        return cls._instancia

    def __setitem__(self, chave: str, valor: str):
        self._variaveis[chave] = valor

    def __getitem__(self, chave: str) -> str:
        return self._variaveis[chave]


