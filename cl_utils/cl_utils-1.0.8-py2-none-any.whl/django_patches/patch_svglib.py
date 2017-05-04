
def _patch_font(self, svgAttr):
    font_mapping = {'sans-serif': 'Helvetica',
                    'serif': 'Times-Roman',
                    'monospace': 'Courier'}

    font_name = font_mapping.get(svgAttr, svgAttr)

    from reportlab.pdfbase.pdfmetrics import getTypeFace

    try:
        getTypeFace(font_name)
    except KeyError:
        font_name = 'Helvetica'

    return font_name

def patch():
    import warnings
    warnings.warn('custom svglib is used; patch this there', PendingDeprecationWarning)
    from svglib.svglib import Svg2RlgAttributeConverter
    setattr(Svg2RlgAttributeConverter, 'convertFontFamily', _patch_font)

