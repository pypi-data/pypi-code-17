import re
from typing import List


def find_indexes(haystack: List[str], regex: str) -> List[int]:
    """
    Find indexes in a list where a regular expression matches.

    Parameters
    ----------
    haystack
        List of strings.
    regex
        Regular expression to match.

    Returns
    -------
        The indexes where the regular expression was found.
    """
    return [i for i, item in enumerate(haystack) if re.search(regex, item)]


def find_style_file(filename, config):
    """
    TODO
    """
    outpath = config['local_path'] / 'out'
    filepath = outpath / config['style_path'] / config[filename]
    if not filepath.exists():
        filepath = outpath / 'markdownrevealstyle' / config[filename]
    if not filepath.exists():
        return
    return filepath.relative_to(filepath.parents[1])


def tweak_html_footer(html, footer):
    """
    TODO
    """
    if not footer:
        return False
    text = '<div class="footer">%s</div>' % footer
    for index in find_indexes(html, '<div class=\"reveal\">'):
        html.insert(index + 1, text)
    return True


def tweak_html_header(html, header):
    """
    TODO
    """
    if not header:
        return
    text = '<div class="header">%s</div>' % header
    for index in find_indexes(html, '<div class=\"reveal\">'):
        html.insert(index + 1, text)


def tweak_html_warmup(html, config):
    """
    TODO
    """
    fname = find_style_file('style_warmup', config)
    if not fname:
        return
    text = '<section><img src="%s" /></section>' % fname
    index = find_indexes(html, 'div class="slides"')[0]
    html.insert(index + 1, text)


def tweak_html_logo(html, config):
    """
    TODO
    """
    fname = find_style_file('style_logo', config)
    if not fname:
        return
    text = '<div class="logo"><img src="%s" /></div>' % fname
    for index in find_indexes(html, '<div class=\"reveal\">'):
        html.insert(index + 1, text)


def tweak_html_background(html, config):
    """
    TODO
    """
    fname = find_style_file('style_background', config)
    if not fname:
        return
    text = '<section data-background="%s">' % fname
    for index in find_indexes(html, '<section>'):
        html[index] = html[index].replace('<section>', text)


def tweak_html_emoji_set(html, config):
    """
    TODO
    """
    if not config['emoji_set']:
        return
    index = find_indexes(html, 'stylesheet.*id="theme"')[0]
    emoji_tweaks = '''
<script src="https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/lib/js/emojione.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/css/emojione.min.css" />

<style type="text/css">
img.emojione {
  /* Override any img styles to ensure Emojis are displayed inline */
  height: 1em;
  margin: 0px !important;
/*  display: inline !important; */
/*  min-width: 15px!important; */
/*  min-height: 15px!important; */
  vertical-align: middle;
}
</style>
<script type="text/javascript">
document.addEventListener("DOMContentLoaded", function convert() {
    emojione.imageType = 'svg';
    var input = document.body.innerHTML;
    var output = emojione.unicodeToImage(input);
    document.body.innerHTML = output;
});
</script>
    '''
    html.insert(index, emoji_tweaks)
    return True


def tweak_html_css(html, config):
    """
    TODO
    """
    fname = find_style_file('style_custom_css', config)
    if not fname:
        return
    index = find_indexes(html, 'stylesheet.*id="theme"')[0]
    text = '<link rel="stylesheet" href="%s">' % fname
    html.insert(index + 1, text)
    return True


def tweak_html(html, config):
    """
    TODO
    """
    html = html.splitlines()
    # TODO: footer and header could be added to the style template (i.e.:
    #       within a config.yaml file part of the template which Markdownreveal
    #       should be able to load and override if necessary)
    tweak_html_footer(html, config['footer'])
    tweak_html_header(html, config['header'])
    tweak_html_warmup(html, config)
    tweak_html_logo(html, config)
    tweak_html_background(html, config)
    tweak_html_emoji_set(html, config)
    tweak_html_css(html, config)
    return '\n'.join(html)
