"""
@file
@brief Simple wrapper for `treant-js <http://fperucic.github.io/treant-js/>`_.
"""

_template_html = """
<style>
__STYLE__
</style>

<link rel="stylesheet" href="http://fperucic.github.io/treant-js/Treant.css">
<script src="http://fperucic.github.io/treant-js/vendor/raphael.js"></script>
<script src="http://fperucic.github.io/treant-js/Treant.js"></script>
<div class="__CLASSCHART__" id="__DIVID__"></div>
"""

_template_js = """
var tree_structure__DIVID__ = {
    __CLASSCHART__: __JSONCHART__,
    nodeStructure: __JSONDATA__
};
new Treant( tree_structure__DIVID__ );
"""


def display_treant(json_tree, json_data, css, classname):
    """
    Display a chart using `treant-js <http://fperucic.github.io/treant-js/>`_.

    @param  json_tree       json which describe global attributes of the tree
    @param  json_data       json which describe the tree structures
    @param  css             style
    @param  classname       class name associated to the section DIV which will receive the
                            tree
    @return                 HTML object
    """

    global _template_html, _template_js
    uid = "id_" + str(id(json_data))

    # this should be done with jinja2 or mako
    ht = _template_html.replace("__STYLE__", css) \
        .replace("__CLASSCHART__", classname) \
        .replace("__JSONCHART__", json_tree) \
        .replace("__JSONDATA__", json_data) \
        .replace("__DIVID__", uid)
    jv = _template_js.replace("__STYLE__", css) \
        .replace("__CLASSCHART__", classname) \
        .replace("__JSONCHART__", json_tree) \
        .replace("__JSONDATA__", json_data) \
        .replace("__DIVID__", uid)

    from IPython.core.display import HTML
    return HTML(ht + "<script>" + jv + "</script>")
