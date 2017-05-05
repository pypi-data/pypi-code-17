from .numvalue import Number, Integer
from .formvalue import String, Dropdown, Checkbox, Radiobuttons, Togglebuttons, Text
from .group import Tab, Form
from .upload import FileUpload
from .editor import Editor

from IPython.display import HTML, Javascript, display
from string import Template

js_template = """
<script type="text/Javascript">
function push_button(){
    var command = "${cb}";
    console.log("Executing Command: " + command);
    var kernel = IPython.notebook.kernel;
    kernel.execute(command);
    }
</script>
"""

html = """<button onclick="push_button()">${name}</button>"""

class Button(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.cb = kwargs.get('cb', None)
        self.desc = kwargs.get('desc', '')

        d = dict(name=self.name)
        h = Template(html).substitute(d)
        display(HTML(h))
        d = dict(cb=self.cb)
        js = Template(js_template).substitute(d)
        display(HTML(js))
