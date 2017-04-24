import unittest
from unittest import mock

from codeskeleton import exceptions
from codeskeleton import spec


class TestDefault(unittest.TestCase):
    def test_deserialize(self):
        default = spec.Default(variables=mock.MagicMock())
        default.deserialize(data={'value': 'testvalue', 'variable': 'testvariable'})
        self.assertEqual(default.variable, 'testvariable')
        self.assertEqual(default.value, 'testvalue')

    def test_get_value_value(self):
        default = spec.Default(variables=mock.MagicMock(), value='testvalue')
        self.assertEqual(default.get_value(), 'testvalue')

    def test_get_value_variable(self):
        variables = spec.Variables(spec.Variable(name='testvariable', value='variablevalue'))
        default = spec.Default(variables=variables, variable='testvariable')
        self.assertEqual(default.get_value(), 'variablevalue')

    def test_validate_spec_invalid_variable(self):
        variables = spec.Variables()
        default = spec.Default(variables=variables, variable='testvariable')
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    "Invalid variable referenced by default: 'testvariable'"):
            default.validate_spec(path='test')
