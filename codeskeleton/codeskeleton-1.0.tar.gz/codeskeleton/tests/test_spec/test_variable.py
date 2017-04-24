import unittest
from unittest import mock

from codeskeleton import exceptions
from codeskeleton import spec


class TestVariable(unittest.TestCase):
    def test_deserialize_empty_data(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname')
        variable.deserialize(data={})
        self.assertEqual(variable.name, 'testname')
        self.assertEqual(variable.default, None)
        self.assertEqual(len(variable.validators), 0)
        self.assertEqual(variable.help_text, None)
        self.assertEqual(variable.generator, None)
        self.assertEqual(variable.arguments, None)

    def test_deserialize_default(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname')
        variable.deserialize(data={'default': {'value': 'the default'}})
        self.assertEqual(variable.default.value, 'the default')

    def test_deserialize_validators(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname')
        variable.deserialize(data={'validators': {'email': {}}})
        self.assertEqual(len(variable.validators), 1)

    def test_deserialize_help_text(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname')
        variable.deserialize(data={'help_text': 'some help'})
        self.assertEqual(variable.help_text, 'some help')

    def test_deserialize_generator(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname')
        variable.deserialize(data={'generator': 'random_alphanumeric_string'})
        self.assertEqual(variable.generator, 'random_alphanumeric_string')

    def test_deserialize_arguments(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname')
        variable.deserialize(data={'arguments': {'length': 10}})
        self.assertEqual(variable.arguments, {'length': 10})

    def test_is_required_has_default_false(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname',
                                 default=spec.Default(variables=mock.MagicMock()))
        self.assertFalse(variable.is_required())

    def test_is_required_no_default_true(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname')
        self.assertTrue(variable.is_required())

    def test_takes_input_has_generator_false(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname',
                                 generator='random_alphanumeric_string')
        self.assertFalse(variable.takes_input())

    def test_takes_input_no_generator_true(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname')
        self.assertTrue(variable.takes_input())

    def test_set_value(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname')
        variable.set_value('testvalue')
        self.assertEqual(variable.value, 'testvalue')

    def test_get_value_has_value(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname',
                                 value='testvalue')
        self.assertEqual(variable.get_value(), 'testvalue')

    def test_get_value_has_default(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname',
                                 default=spec.Default(variables=mock.MagicMock(),
                                                      value='defaultvalue'))
        self.assertEqual(variable.get_value(), 'defaultvalue')

    def test_get_value_has_default_and_value(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname',
                                 default=spec.Default(variables=mock.MagicMock(),
                                                      value='defaultvalue'),
                                 value='testvalue')
        self.assertEqual(variable.get_value(), 'testvalue')

    def test_get_value_has_generator(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname',
                                 generator='debug')
        self.assertEqual(variable.get_value(), 'DEBUG')

    def test_get_value_has_generator_with_arguments(self):
        variable = spec.Variable(variables=mock.MagicMock(), name='testname',
                                 generator='debug',
                                 arguments={'suffix': 'xx'})
        self.assertEqual(variable.get_value(), 'DEBUGxx')

    def test_validate_spec_both_generator_and_default(self):
        variables = spec.Variables()
        variable = spec.Variable(variables=variables, name='testname',
                                 generator='debug',
                                 default=spec.Default(variables=mock.MagicMock()))
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    'Can not provide both "default" and "generator".'):
            variable.validate_spec(path='test')

    def test_validate_spec_invalid_generator(self):
        variables = spec.Variables()
        variable = spec.Variable(variables=variables, name='testname',
                                 generator='invalidgenerator')
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    "Invalid generator: 'invalidgenerator'. Must be one of:"):
            variable.validate_spec(path='test')

    def test_validate_spec_arguments_without_generator(self):
        variables = spec.Variables()
        variable = spec.Variable(variables=variables, name='testname',
                                 arguments={'a': 10})
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    'Can not use "arguments" without a "generator".'):
            variable.validate_spec(path='test')

    def test_validate_value_invalid(self):
        variables = spec.Variables()
        variable = spec.Variable(variables=variables, name='testname',
                                 validators=spec.ValueValidators({
                                     'one_letter': {}
                                 }))
        with self.assertRaisesRegex(exceptions.ValueValidationError,
                                    'Must be exactly one letter'):
            variable.validate_value(value='xx')

    def test_validate_value_valid(self):
        variables = spec.Variables()
        variable = spec.Variable(variables=variables, name='testname',
                                 validators=spec.ValueValidators({
                                     'one_letter': {}
                                 }))
        variable.validate_value(value='x')

    def test_validate_value_no_validators(self):
        variables = spec.Variables()
        variable = spec.Variable(variables=variables, name='testname')
        variable.validate_value(value='x')
