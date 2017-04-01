import pytest

from zeep import Client


def test_factory_namespace():
    client = Client('tests/wsdl_files/soap.wsdl')
    factory = client.type_factory('http://example.com/stockquote.xsd')
    obj = factory.Address(NameFirst='Michael', NameLast='van Tellingen')
    assert obj.NameFirst == 'Michael'
    assert obj.NameLast == 'van Tellingen'


def test_factory_ns_auto_prefix():
    client = Client('tests/wsdl_files/soap.wsdl')
    factory = client.type_factory('ns0')
    obj = factory.Address(NameFirst='Michael', NameLast='van Tellingen')
    assert obj.NameFirst == 'Michael'
    assert obj.NameLast == 'van Tellingen'


def test_factory_ns_custom_prefix():
    client = Client('tests/wsdl_files/soap.wsdl')
    client.set_ns_prefix('sq', 'http://example.com/stockquote.xsd')
    factory = client.type_factory('sq')
    obj = factory.Address(NameFirst='Michael', NameLast='van Tellingen')
    assert obj.NameFirst == 'Michael'
    assert obj.NameLast == 'van Tellingen'


def test_factory_ns_unknown_prefix():
    client = Client('tests/wsdl_files/soap.wsdl')

    with pytest.raises(ValueError):
        client.type_factory('bla')
