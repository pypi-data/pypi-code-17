import unittest

from .population_schema import ColumnDefinition, PopulationSchema


class PopulationSchemaTest(unittest.TestCase):

    def test_column_definition_eq(self):  # type: () -> None
        self.assertEqual(
            ColumnDefinition('a', 'sequence', length=4),
            ColumnDefinition('a', 'sequence', length=4, transform='identity'))
        self.assertNotEqual(
            ColumnDefinition('a', 'sequence', length=4),
            ColumnDefinition('a', 'sequence', length=3))

    def test_population_schema_eq(self):  # type: () -> None
        s1 = PopulationSchema({'a': ColumnDefinition('a', 'realAdditive')}),
        s2 = PopulationSchema({'a': ColumnDefinition('a', 'realAdditive')}),
        s3 = PopulationSchema({'b': ColumnDefinition('b', 'realAdditive')})
        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)


if __name__ == '__main__':
    unittest.main()
