from __future__ import unicode_literals, print_function
import click
from pathlib import Path

def read_spex_file(filename):
    from .base import load_spexcript
    with open(str(filename), "r", encoding = 'utf8') as f:
        spexcript = load_spexcript(f)
    return spexcript # the spex itself

@click.command()
@click.argument('inputfile', type=click.Path(exists=True,
                                             readable=True,
                                             dir_okay=False),)
                #help="Spexcript source file (utf8-encoded text)")
def main(inputfile):
    """Generate a clean pdf from a spexcript source file (utf-8-encoded)."""

    inputfile = Path(inputfile)
    try:
        spex = read_spex_file(inputfile)
    except FileNotFoundError:
        print("File '" + filename + "' not found")
        return -1
    from .language import Finnish
    from . import latex
    spextex = latex.Spextex(Finnish)
    spex.generate_front_page(spextex)
    spex.generate_characters(spextex)
    spex.generate_listing(spextex)
    spex.generate_script(spextex)
    tex = spextex.final_result()
    latex.pdflatex(tex, outputfile=inputfile.with_suffix(".pdf"))
    return 0


if __name__ == "__main__":
    import sys
    sys.argv[0] = "spexcript"
    sys.exit(main())
