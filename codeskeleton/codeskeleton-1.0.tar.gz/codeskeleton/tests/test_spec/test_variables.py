import unittest
from collections import OrderedDict

from codeskeleton import exceptions
from codeskeleton import spec


class TestVariables(unittest.TestCase):
    def test_deserialize_empty_data(self):
        variables = spec.Variables()
        variables.deserialize(data={})
        self.assertEqual(variables._variables, OrderedDict())

    def test_deserialize_one_value(self):
        variables = spec.Variables()
        variables.deserialize(data={
            'testvariable': {}
        })
        self.assertEqual(len(variables._variables), 1)
        self.assertIn('testvariable', variables._variables)
        self.assertIsInstance(variables._variables['testvariable'], spec.Variable)
        self.assertEqual(variables._variables['testvariable'].name, 'testvariable')

    def test_deserialize_multiple_values(self):
        variables = spec.Variables()
        variables.deserialize(data={
            'testvariable1': {},
            'testvariable2': {},
        })
        self.assertEqual(len(variables._variables), 2)
        self.assertIn('testvariable1', variables._variables)
        self.assertIn('testvariable2', variables._variables)

    def test_get_variable(self):
        variables = spec.Variables()
        variables._variables['testvariable'] = spec.Variable(name='testvariable')
        self.assertEqual(variables.get_variable('testvariable').name, 'testvariable')

    def test_get_variable_invalid_name(self):
        variables = spec.Variables()
        with self.assertRaisesRegex(exceptions.InvalidVariableName,
                                    'Invalid variable name: testvariable'):
            variables.get_variable('testvariable')

    def test_get_variable_value(self):
        variables = spec.Variables()
        variables._variables['testvariable'] = spec.Variable(name='testvariable', value='test')
        self.assertEqual(variables.get_variable_value('testvariable'), 'test')

    def test_get_variable_value_invalid_name(self):
        variables = spec.Variables()
        with self.assertRaisesRegex(exceptions.InvalidVariableName,
                                    'Invalid variable name: testvariable'):
            variables.get_variable_value('testvariable')

    def test_has_variable_true(self):
        variables = spec.Variables()
        variables._variables['testvariable'] = spec.Variable(name='testvariable', value='test')
        self.assertTrue(variables.has_variable('testvariable'))

    def test_has_variable_false(self):
        variables = spec.Variables()
        self.assertFalse(variables.has_variable('testvariable'))

    def test_set_variable_values(self):
        variables = spec.Variables()
        variables._variables['testvariable1'] = spec.Variable(name='testvariable')
        variables._variables['testvariable2'] = spec.Variable(name='testvariable')
        self.assertEqual(variables._variables['testvariable1'].value, None)
        self.assertEqual(variables._variables['testvariable2'].value, None)
        variables.set_variable_values(testvariable1='a', testvariable2='b')
        self.assertEqual(variables._variables['testvariable1'].value, 'a')
        self.assertEqual(variables._variables['testvariable2'].value, 'b')

    def test_add_variable(self):
        variable = spec.Variable(name='testvariable')
        variables = spec.Variables()
        variables.add_variable(variable)
        self.assertEqual(variables._variables['testvariable'], variable)

    def test_add_variables(self):
        variable1 = spec.Variable(name='testvariable1')
        variable2 = spec.Variable(name='testvariable2')
        variables = spec.Variables()
        variables.add_variables(variable1, variable2)
        self.assertEqual(len(variables._variables), 2)
        self.assertEqual(variables._variables['testvariable1'], variable1)
        self.assertEqual(variables._variables['testvariable2'], variable2)

    def test_values_as_dict(self):
        variable1 = spec.Variable(name='testvariable1', value='a')
        variable2 = spec.Variable(name='testvariable2', value='b')
        variables = spec.Variables(variable1, variable2)
        self.assertEqual(variables.values_as_dict(), {
            'testvariable1': 'a',
            'testvariable2': 'b'
        })

    def test_iterate_input_variables(self):
        variable1 = spec.Variable(name='testvariable1', value='a')
        variable2 = spec.Variable(name='testvariable2', value='b')
        variable3 = spec.Variable(name='testvariable3', generator='debug')
        variables = spec.Variables(variable1, variable2, variable3)
        input_variables = list(variables.iterate_input_variables())
        self.assertEqual(input_variables, [variable1, variable2])
