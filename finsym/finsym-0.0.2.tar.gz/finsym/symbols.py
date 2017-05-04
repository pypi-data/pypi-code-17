class Symbol(object):
    """
    Base class for all symbols.
    """
    # Setting a class attribute __symbol__ doesn't show-up in
    # calls to __dict__. Investigate the usefulness of being able
    # to call an attribute to determine if a thing "is-a"
    # __symbol__ = True
    def __init__(self, ticker, symbology):
        self._ticker = ticker
        self.symbology = symbology

    @property
    def ticker(self):
        """
        Unique identifier for a Symbol within a given
        symbology.
        """
        return self._ticker

    def __str__(self):
        return self.ticker

    def __repr__(self):
        return "Symbol(%s, %s)" % (self.ticker, self.symbology)


class FinancialSymbol(Symbol):
    """
    A FinancialSymbol is the base representation for a
    SecuritySymbol and and ContractSymbol.
    """
    def __init__(self, ticker, symbology, base=None, suffix=''):
        super(FinancialSymbol, self).__init__(ticker, symbology)
        self._ticker = ticker
        self.symbology = symbology
        self._base = base or self._ticker
        self._suffix = suffix

    @property
    def base(self):
        return self._base

    @property
    def suffix(self):
        return self._suffix


class SecuritySymbol(FinancialSymbol):
    """
    A SecuritySymbol is a FinancialSymbol that represents the namespace for
    a set of ContractSymbols
    """
    def __init__(self, ticker, symbology, security_id, base=None, suffix=''):
        super(SecuritySymbol, self).__init__(ticker, symbology, base=base, suffix=suffix)
        self.security_id = security_id

    def __eq__(self, other):
        # Think about this a bit more. Is this correct?
        same = (self.symbology == other.symbology) and (self.security_id == other.security_id)
        return same


class ContractSymbol(FinancialSymbol):
    """
    A ContractSymbol is a FinancialSymbol that resides in a SecuritySymbol
    namespace. In the real world a ContractSymbol represents a thing that
    can actually be traded.
    """
    def __init__(self, ticker, symbology, security_symbol, base=None, suffix=''):
        super(ContractSymbol, self).__init__(ticker, symbology, base=base, suffix=suffix)
        self.security_symbol = security_symbol

    def __eq__(self, other):
        # Think about this a bit more. Is this correct?
        same_security = self.security_symbol == other.security_symbol
        same_ticker = self.ticker == other.ticker
        same = same_ticker and same_security
        return same


def is_symbol(dct):
    """
    Helper function for serialization. True if contents
    of dct contains identifier for a Symbol object.
    """
    return '__symbol__' in dct and dct['__symbol__']


def is_financial_symbol(dct):
    """
    Helper function for serialization. True if contents
    of dct contains identifier for a FinancialSymbol object.
    """
    return '__financial_symbol__' in dct and dct['__financial_symbol__']


def is_security_symbol(dct):
    """
    Helper function for serialization. True if contents
    of dct contains identifier for a SecuritySymbol object.
    """
    return '__security_symbol__' in dct and dct['__security_symbol__']


def is_contract_symbol(dct):
    """
    Helper function for serialization. True if contents
    of dct contains identifier for a ContractSymbol object.
    """
    return '__contract_symbol__' in dct and dct['__contract_symbol__']


def symbol_factory(dct):
    """
    Factory method for creating different types of symbols. Useful
    for deserialization
    """
    obj = dct
    if is_symbol(dct):
        obj = Symbol(ticker=dct['_ticker'], symbology=dct['symbology'])
    elif is_financial_symbol(dct):
        obj = FinancialSymbol(ticker=dct['_ticker'], symbology=dct['symbology'],
                              base=dct['_base'], suffix=dct['_suffix'])
    elif is_security_symbol(dct):
        obj = SecuritySymbol(ticker=dct['_ticker'], symbology=dct['symbology'],
                             security_id=dct['security_id'], base=dct['_base'],
                             suffix=dct['_suffix'])
    elif is_contract_symbol(dct):
        obj = ContractSymbol(ticker=dct['_ticker'], symbology=dct['symbology'],
                             security_symbol=dct['security_symbol'], base=dct['_base'],
                             suffix=dct['_suffix'])
    return obj


def from_serialized(dct):
    return symbol_factory(dct)
