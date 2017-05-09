"""
@brief      test log(time=35s)
"""

import sys
import os
import unittest


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_

from pyquickhelper.loghelper import fLOG
from src.jupytalk.talk_examples.treant_wrapper import display_treant


class TestPyData2016treant(unittest.TestCase):

    def test_example_treant(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        css = """
        .chart { height: 600px; width: 900px; margin: 5px; margin: 15px auto; border: 3px solid #DDD; border-radius: 3px; }

        .tennis-draw {
            font-size: 10px;
            width: 100px;
        }

        .tennis-draw.winner { height: 38px; }
        .tennis-draw.winner:hover {
            background: url('http://fperucic.github.io/treant-js/examples/tennis-draw/trophy.png') right 0 no-repeat;
        }
        .tennis-draw.winner .node-name { padding-left: 10px; margin-top: 1px; display: block; }

        .tennis-draw .node-name { padding: 2px; white-space: pre; color: #00AFF0; }
        .tennis-draw .node-desc { padding: 2px; color: #999; }

        .tennis-draw.first-draw .node-title,
        .tennis-draw.first-draw .node-name,
        .tennis-draw.first-draw img { position: absolute; top: -8px; }
        .tennis-draw.first-draw:hover img { width: 20px; top: -12px; }

        .tennis-draw.first-draw { width: 165px; height: 20px; }
        .tennis-draw.first-draw img { margin: 3px 4px 0 0; left: 25px; }
        .tennis-draw.first-draw .node-title { margin-top: 3px; }
        .tennis-draw.first-draw .node-name { width: 113px; padding-left: 50px; }
        .tennis-draw.first-draw.bye .node-name { color: #999; }
        """

        classname = "chart"

        # this part should be part of a nice API (to avoid trick like this
        # __DIVID__)
        json_tree = """{
                container: "#__DIVID__",
                levelSeparation:    20,
                siblingSeparation:  15,
                subTeeSeparation:   15,
                rootOrientation: "EAST",

                node: {
                    HTMLclass: "tennis-draw",
                    drawLineThrough: true
                },
                connectors: {
                    type: "straight",
                    style: {
                        "stroke-width": 2,
                        "stroke": "#ccc"
                    }
                }
            }"""

        # there should a nice API to define that
        json_data = """{
                text: {
                    name: {val: "Djokovic, Novak",
                           href: "http://www.atpworldtour.com/Tennis/Players/Top-Players/Novak-Djokovic.aspx"}
                },
                HTMLclass: "winner",
                children: [
                    {
                        text: {
                            name: "Djokovic, Novak",
                            desc: "4-6, 6-2, 6-2"
                        },
                        children: [
                            {
                                text: {
                                    name: "Djokovic, Novak",
                                    desc: "4-6, 6-1, 6-4"
                                },
                                children: [
                                    {
                                        text: {
                                            name: "Djokovic, Novak",
                                            desc: "4-6, 6-1, 6-4"
                                        },
                                        children: [
                                            {
                                                text: {
                                                    name: "Djokovic, Novak",
                                                    title: 1
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/srb.jpg",
                                                HTMLclass: "first-draw",
                                            },
                                            {
                                                text: {
                                                    name: "Bye",
                                                    title: 2
                                                },
                                                HTMLclass: "first-draw bye"
                                            }
                                        ]
                                    },
                                    {
                                        text: {
                                            name: "Youzhny, Mikhail",
                                            desc: "6-4, 6-0"
                                        },
                                        children: [
                                            {
                                                text: {
                                                    name: "Youzhny, Mikhail",
                                                    title: 3
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/rus.jpg",
                                                HTMLclass: "first-draw"
                                            },
                                            {
                                                text: {
                                                    name: "Gimeno-Traver, Daniel",
                                                    title: 4
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/esp.jpg",
                                                HTMLclass: "first-draw"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                text: {
                                    name: "Monaco, Juan",
                                    desc: "6-0, 3-6, 6-3"
                                },
                                children: [
                                    {
                                        text: {
                                            name: "Gulbis, Ernests",
                                            desc: "4-6, 6-2, 6-3"
                                        },
                                        children: [
                                            {
                                                text: {
                                                 name: "Gulbis, Ernests",
                                                 title: 5
                                             },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/lat.jpg",
                                                HTMLclass: "first-draw"
                                            },
                                            {
                                                text: {
                                                    name: "Isner, John",
                                                    title: 6
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/usa.jpg",
                                                HTMLclass: "first-draw"
                                            }
                                        ]
                                    },
                                    {
                                        text: {
                                            name: "Monaco, Juan",
                                            desc: "6-4, 6-0"
                                        },
                                        children: [
                                            {
                                                text: {
                                                    name: "Klizan, Martin",
                                                    title: 7
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/slo.jpg",
                                                HTMLclass: "first-draw"
                                            },
                                            {
                                                text: {
                                                    name: "Monaco, Juan",
                                                    title: 8
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/arg.jpg",
                                                HTMLclass: "first-draw"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        text: {
                            name: "Nieminen, Jarkko",
                            desc: "6-3, 1-6, 7-6(3)"
                        },
                        children: [
                            {
                                text: {
                                    name: "Nieminen, Jarkko",
                                    desc: "4-6, 6-1, 6-4"
                                },
                                children: [
                                    {
                                        text: {
                                            name: "Raonic, Milos",
                                            desc: "6-1, 6-4"
                                        },
                                        children: [
                                            {
                                                text: {
                                                    name: "Raonic, Milos",
                                                    title: 9
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/can.jpg",
                                                HTMLclass: "first-draw"
                                            },
                                            {
                                                text: {
                                                    name: "Benneteau, Julien",
                                                    title: 10
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/fra.jpg",
                                                HTMLclass: "first-draw"
                                            }
                                        ]
                                    },
                                    {
                                        text: {
                                            name: "Nieminen, Jarkko",
                                            desc: "6-1, 6-2"
                                        },
                                        children: [
                                            {
                                                text: {
                                                    name: "Nieminen, Jarkko",
                                                    title: 11
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/fin.jpg",
                                                HTMLclass: "first-draw"
                                            },
                                            {
                                                text: {
                                                    name: "Troicki, Viktor",
                                                    title: 12
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/srb.jpg",
                                                HTMLclass: "first-draw"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                text: {
                                    name: "Del Potro, Juan Martin",
                                    desc: "6-2, 6-4"
                                },
                                children: [
                                    {
                                        text: {
                                            name: "Dolgopolov, Alexandr",
                                            desc: "4-6, 6-2, 6-3"
                                        },
                                        children: [
                                            {
                                                text: {
                                                    name: "Dolgopolov, Alexandr",
                                                    title: 13
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/ukr.jpg",
                                                HTMLclass: "first-draw"
                                            },
                                            {
                                                text: {
                                                    name: "Tomic, Bernard",
                                                    title: 14
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/aus.jpg",
                                                HTMLclass: "first-draw"
                                            }
                                        ]
                                    },
                                    {
                                        text: {
                                            name: "Del Potro, Juan Martin",
                                            desc: "6-4, 6-0"
                                        },
                                        children: [
                                            {
                                                text: {
                                                    name: "Bye",
                                                    title: 15
                                                },
                                                HTMLclass: "first-draw bye"
                                            },
                                            {
                                                text: {
                                                    name: "Del Potro, Juan Martin",
                                                    title: 16
                                                },
                                                image: "http://fperucic.github.io/treant-js/examples/tennis-draw/flags/arg.jpg",
                                                HTMLclass: "first-draw"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }"""

        h = display_treant(json_tree, json_data, css, classname)
        assert h


if __name__ == "__main__":
    unittest.main()
