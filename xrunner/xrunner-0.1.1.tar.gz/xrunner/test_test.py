from test import Test
from nose.tools import assert_equal

# Tests Test class


class TestTest:

    def __init__(self):
        self.default_url_prefix = "http://localhost:5000"
        self.tests = [
            {"test": [
                {
                    "name": "Sample XML search API",
                }, {
                    "url": "/sample/search/test?wt=xml",
                }, {
                    "group": "SAMPLE TEST",
                }, {
                    "method": "GET",
                }, {
                    "validators": [
                        {
                            "compare": {
                                "xpath": "/response/lst[@name='searchMetaData']/int[@name='status']",
                                "comparator": "eq",
                                "type": "text",
                                "expected": "0",
                            },
                        },
                    ],
                },
            ], "assert": True,
            }, { "test" : [
                {
                    "name": "Sample XML search API for products",
                }, {
                    "url": "/sample/products?q=black%20tote&wt=xml",
                }, {
                    "group": "SAMPLE TEST",
                }, {
                    "method": "GET",
                }, {
                    "validators": [
                        {
                            "compare": {
                                "xpath": "/response/result/@numberOfProducts",
                                "comparator": "eq",
                                "type": "element",
                                "expected": "7",
                            },
                        },
                    ],
                },
            ], "assert" : True,
            }, { "test": [
                {
                    "name": "XML search with products",
                }, {
                    "url": "/sample/products?q=shirts&wt=xml",
                }, {
                    "group": "SAMPLE TEST",
                }, {
                    "method": "GET",
                }, {
                    "validators": [
                        {
                            "compare": {
                                "xpath": "(//product/str[@name='uniqueId'])[2]",
                                "comparator": "eq",
                                "type": "text",
                                "expected": "9543",
                            },
                        },
                    ],
                },
            ], "assert" : True
            }, { "test" : [
                {
                    "name": "XML search with products",
                }, {
                    "url": "/sample/products?q=shirts&wt=xml",
                }, {
                    "group": "SAMPLE TEST",
                }, {
                    "method": "GET",
                }, {
                    "validators": [
                        {
                            "compare": {
                                "xpath": "(//product/str[@name='sku'])[3]",
                                "comparator": "eq",
                                "type": "text",
                                "expected": 'M805',
                            },
                        },
                    ],
                },
            ], "assert": True
            }
        ]

    def __load_data__(self, test_data):
        return_data = {}
        for td in test_data:
            if 'name' in td:
                return_data['name'] = td['name']
            if 'url' in td:
                return_data['url'] = td['url']
            if 'group' in td:
                return_data['group'] = td['group']
            if 'method' in td:
                return_data['method'] = td['method']
            if 'validators' in td:
                return_data['validators'] = td['validators']
        return return_data

    def test_init(self):
        data = [
            {
                "name": "XML Search API Validation for test search API",
            }, {
                "url": "/sample/search/test?wt=xml",
            }, {
                "group": "SAMPLE TEST",
            }, {
                "method": "GET",
            }, {
                "validators": [
                    {
                        "compare": {
                            "xpath": "/response/lst[@name='searchMetaData']/int[@name='status']",
                            "comparator": "eq",
                            "type": "text",
                            "expected": '0',
                        },
                    },
                ],
            },
        ]

        t = Test(data, self.default_url_prefix)
        test_data = self.__load_data__(data)
        assert_equal(t.to_string(), test_data['name'] + " "
                     + self.default_url_prefix + test_data['url']
                     + " " + test_data['group'] + " " + test_data['method']
                     + " " + 'compare' + " " + "xpath" + " "
                     + test_data['validators'][0]['compare']['xpath'] + " "
                     + test_data['validators'][0]['compare']['comparator'] + " "
                     + test_data['validators'][0]['compare']['type'])

    def test_run(self):
        for test in self.tests:
            t = Test(test['test'], self.default_url_prefix)
            assert_equal(t.run(), test['assert'])
