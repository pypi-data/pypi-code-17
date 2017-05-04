import symbols
import functools


@functools.singledispatch
def to_serializable(val):
    """
    Used by default.
    """
    return str(val)


@to_serializable.register(symbols.Symbol)
def ts_symbol(val):
    dct = val.__dict__
    dct.update({"__symbol__": True})
    return dct


@to_serializable.register(symbols.FinancialSymbol)
def ts_financial_symbol(val):
    dct = val.__dict__
    dct.update({"__financial_symbol__": True})
    return dct


@to_serializable.register(symbols.SecuritySymbol)
def ts_security_symbol(val):
    dct = val.__dict__
    dct.update({"__security_symbol__": True})
    return dct


@to_serializable.register(symbols.ContractSymbol)
def ts_contract_symbol(val):
    dct = val.__dict__
    dct.update({"__contract_symbol__": True})
    return dct
