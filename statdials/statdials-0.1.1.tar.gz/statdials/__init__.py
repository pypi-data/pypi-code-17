import tempfile
import os
import shutil

from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape
from pylatex.package import Package
from pylatex.base_classes import Environment, CommandBase
from pylatex.tikz import TikZ


class StatDial(CommandBase):
    packages = [Package('statdials')]
    _latex_name = 'statdial'
    _default_escape = False


class StatDials(object):

    def __init__(self, data):
        self.data = data

    def generate_pdf(self, filename=None):

        if filename is None:
            filename = os.path.join(tempfile.mkdtemp(), 'standalone')

        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'statdials.sty'), os.path.join(os.path.dirname(os.path.abspath(filename)), 'statdials.sty'))

        standalone = Document(filename, documentclass='standalone')

        with standalone.create(TikZ(options='text centered')):
            for i, row in enumerate(self.data):
                for j, dial in enumerate(row):
                    assert isinstance(dial, dict)
                    standalone.append(StatDial(
                        options=[
                            'position={(%d,-%d)}' % (j*3, i*3),
                            'weight=%s' % dial.get('weight', 1),
                            'weightOffset=%s' % dial.get('weightOffset', 0),
                            'color=%s' % dial.get('color', 'statdialSigPos'),
                            'uncertainty=%s' % dial['uncertainty'] if 'uncertainty' in dial else ''
                        ],
                        arguments=dial['metric']
                    ))

        standalone.generate_pdf()

        return '%s.pdf' % filename

    def generate_png(self, filename=None, resolution=300):
        pdf_location = self.generate_pdf()
        from wand.image import Image
        img = Image(filename=pdf_location, resolution=resolution)

        if filename:
            img.save(filename=filename)
        else:
            return img
