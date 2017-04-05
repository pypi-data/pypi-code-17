from rng_to_form.rng import RNG
from rng_to_form.form_maker import make_form, make_tree, set_in_nested_dict, order_dicts, dict_path
from unittest import TestCase, main
from collections import OrderedDict


class RngTest(TestCase):

    def setUp(self):
        self.file = "./tests/data/test.rng"
        self.rng = RNG(file=self.file, target="ArchiveTransfer")

    def test_generate_form(self):
        generated_form = make_form(self.rng)
        self.assertIsNotNone(generated_form)
        self.assertTrue('''<div class="Comment_N65541"><div style='font-weight:bold;'>Comment_N65541.value</div><input class='selectable' value="My comment" style='width:87%' name="Comment_N65541" readonly></div></div>''' in generated_form)

    def test_make_tree(self):
        tree = make_tree({'a.b': 1, 'a.c': 2, 'b.d': 1, 'b.e.a': 1, 'b.e.b': 2})
        self.assertEqual(tree, {'a': {'c': {}, 'b': {}}, 'b': {'d': {}, 'e': {'b': {}, 'a': {}}}})

    def test_set_in_nested_dict(self):
        data = {'a.b': 1, 'a.c': 2, 'b.d': 1, 'b.e.a': 1, 'b.e.b': 2}
        tree = make_tree(data)
        set_in_nested_dict(tree, data)
        self.assertEqual(tree, {'b': {'e': {'b': {'value': 2}, 'a': {'value': 1}}, 'd': {'value': 1}}, 'a': {'c': {'value': 2}, 'b': {'value': 1}}})

    def test_order_dicts(self):
        data = {"Comment_N65541": "foo"}
        tree = make_tree(data)
        set_in_nested_dict(tree, data)
        order = self.rng.find_definitions()
        all_data = {self.rng.get_form_root(root_name="ArchiveTransfer"): tree}
        final = order_dicts(all_data, ordered=order)
        self.assertEqual(final, OrderedDict([('ArchiveTransfer_N65537', OrderedDict([('Comment_N65541', 'foo')]))]))

    def test_dict_path(self):
        res = {}
        for key, value in dict_path({'a': {'b': 1, 'c': 2}, 'b': {'d': 1, 'e': {'a': 1, 'b': 2}}}, path=None):
            res[key] = value
        self.assertEqual(res, {'a.b': 1, 'a.c': 2, 'b.d' : 1, 'b.e.a': 1, 'b.e.b': 2})

if __name__ == '__main__':
    main()
