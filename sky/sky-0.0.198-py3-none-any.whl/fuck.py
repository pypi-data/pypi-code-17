from scraper import Scraper
from crawler import crawl

DEFAULT_CRAWL_CONFIG = {
    # Required
    'seed_urls': [

    ],

    'collections_path': '',

    'collection_name': '',

    # Optional

    'crawl_filter_regexps': [

    ],

    'crawl_required_regexps': [
    ],

    'index_filter_regexps': [

    ],

    'index_required_regexps': [

    ],

    'bad_xpaths': [

    ],

    'overwrite_values_by_xpath': {
        # e.g. 'source_name': '"bla"'
        # e.g. 'publish_date': "substring(//time/@datetime, 1, 10)"
    },

    'max_redirects_per_url': 10,

    'max_tries_per_url': 3,

    'max_workers': 5,

    'max_saved_responses': 20,

    'login_url': '',
    'login_data': {},

    "logging_level": 2,
    # Unimplemented
    'max_hops': 10,

    # Scrape stuff"
    'template_proportion': 0.09,
    'max_templates': 1000
}

# Crawling
CRAWL_CONFIG = DEFAULT_CRAWL_CONFIG
CRAWL_CONFIG.update({
    'seed_urls': [
        'https://recast.ai/mechtecs/pizzabot/learn/time'
    ],

    'collections_path': '/Users/pascal/egoroot/sky_collections',

    'collection_name': 'recast.ai2',

    # Optional

    'crawl_filter_regexps': [

    ],

    'crawl_required_regexps': [

    ],

    'index_filter_regexps': [

    ],

    'index_required_regexps': [
        ""
    ],

    'max_saved_responses': 100,

    'max_workers': 10,
})

crawl.start(CRAWL_CONFIG)

# Indexing

SCRAPE_CONFIG = CRAWL_CONFIG.copy()

SCRAPE_CONFIG.update({
    'template_proportion': 0.09,
    'max_templates': 1000
})

import pdb
pdb.set_trace()


skindex = Scraper(SCRAPE_CONFIG)

skindex.load_local_pages()
skindex.add_template_elements()

res = skindex.process_all(remove_visuals=True)
