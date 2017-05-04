class NaoCarregado(Exception):
    pass


class APIStatusCodes(Exception):
    pass


class TribunalNaoSuportado(APIStatusCodes):
    pass


class ParametrosIncorretos(APIStatusCodes):
    pass


class NaoCadastrado(APIStatusCodes):
    pass


class StatusCodeNaoTratado(Exception):
    pass


class AndamentoSemData(Exception):
    pass
