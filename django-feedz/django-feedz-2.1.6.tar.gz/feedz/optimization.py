import re
#import BeautifulSoup
from bs4 import BeautifulSoup
from bs4.element import Tag
#from HTMLParser import HTMLParseError

#from six.moves.html_parser import HTMLParseError

from django.conf import settings

FEEDZ_REMOVE_TRACKERS = getattr(settings,
    "FEEDZ_REMOVE_TRACKERS", True)

# The obvious tracker images
FEEDZ_TRACKER_SERVICES = getattr(settings,
    "FEEDZ_TRACKER_SERVICES", [
    'http://feedads',
    'http://feeds.feedburner.com/~r/',
    'http://feeds.feedburner.com/~ff/',
    'http://rss.feedsportal.com/c/',
    'http://ads.pheedo.com/',
    'http://a.rfihub.com/',
    'http://segment-pixel.invitemedia.com/',
    'http://pixel.quantserve.com/',
    'http://feeds.newscientist.com/',
    'http://mf.feeds.reuters.com/c/',
    'http://telegraph.feedsportal.com/c/',
])

FEEDZ_SMALL_IMAGE_LIMIT = getattr(settings,
    "FEEDZ_SMALL_IMAGE_LIMIT", 50)


class PostContentOptimizer(object):
    """Remove diverse abberation and annoying content in the posts.

    The idea is to remove some tracker images in the feeds because
    these images are a pollution to the user.

    Identified tools that add tracker images and tools into the feeds

    * Feedburner toolbar -- 4 toolbar images, 1 tracker image.
    * Pheedcontent.com toolbar -- 4 toolbar images, 1 advertisement image.
    * Digg/Reddit generic toolbar - 3 toolbar, no tracker image.
    * http://res.feedsportal.com/ -- 2 toolbar images, 1 tracker image.
    * http://a.rfihub.com/ -- associated with http://rocketfuelinc.com/,
        used for ads or tracking. Not quite sure.

    About 80% of them use feedburner. Few use cases of feeds:

    * feedburner toolbar and tracker

        * WULFMORGENSTALLER
        * MarketWatch.com - Top Stories
        * Hollywood.com - Recent News
        * Wired: entertainement
        * Livescience.com
        * Reader Digest

    * Pheedcontent.com toolbar

        * Sports News : CBSSports.com

    * Digg/Reddit toolbar

        * Abstruse goose

    * http://res.feedsportal.com/

        * New scientist.com

    """

    def looks_like_tracker(self, url):
        """Return True if the image URL has to be removed."""
        for service in FEEDZ_TRACKER_SERVICES:
            if url.startswith(service):
                return True
        return False

    def optimize(self, html, only_visible=True, strip_br=True, strip_container=False):
        """Remove unecessary spaces, <br> and image tracker."""

        # Remove uneccesary white spaces
        html = html.strip()
        if '<' not in html and '>' not in html:
            return html
        tagged = html.startswith('<') and html.endswith('>')

#         try:
        soup = BeautifulSoup(html, 'lxml')#'html5lib')
        self.remove_excessive_br(soup)
        if FEEDZ_REMOVE_TRACKERS:
            self.remove_trackers(soup)
#         except HTMLParseError:# Removed in Python 3.5
#             return html

        if only_visible:
            html = str(soup.findAll('body')[0]).strip()
            html = html[6:-7] # strip <body></body> tags
        else:
            html = str(soup).strip()

        if strip_br:
            html = re.sub(r'<br[^>]+>', '', html, flags=re.M|re.I).strip()

        if not tagged and strip_container:
            html = re.sub(r'^<[^>]+>', '', html)
            html = re.sub(r'<[^>]+>$', '', html)

        return html

    def remove_excessive_br(self, soup):
        # start with true to remove any starting br tag
        last_one_is_br = True
        children = soup.childGenerator()
        for el in children:
            if isinstance(el, Tag):
                if el.name == 'br':
                    if last_one_is_br:
                        el.replaceWith("")
                    last_one_is_br = True
                else:
                    last_one_is_br = False

    def remove_trackers(self, soup):
        """Remove the trackers."""
        stripped_count = 0
        for image in soup("img"):
            already_removed = False

            # remove images that looks like tracker
            image_source = image.get("src", "")
            if len(image_source) == 0 or self.looks_like_tracker(image_source):
                image.replaceWith("")
                already_removed = True

            # remove small images
            try:
                image_width = int(image.get("width",
                    FEEDZ_SMALL_IMAGE_LIMIT))
            except ValueError:
                image_width = None
            if (image_width is not None and
                image_width < FEEDZ_SMALL_IMAGE_LIMIT and
                not already_removed):
                image.replaceWith("")

        # remove links that looks like tracker
        for link in soup("a"):
            link_href = link.get("href")
            if link_href and "://" in link_href:
                if self.looks_like_tracker(link_href):
                    link.replaceWith("")
