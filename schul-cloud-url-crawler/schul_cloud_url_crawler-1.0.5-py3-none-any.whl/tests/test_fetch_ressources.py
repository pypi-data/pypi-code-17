from schul_cloud_url_crawler import fetch



def test_fetch_ressource(ressource, ressource_url):
    """Fetch a ressource."""
    result = fetch([ressource_url])
    assert result.get_ressources() == [ressource]

def test_fetch_ressources(ressources, ressource_urls):
    result = fetch(ressource_urls)
    assert result.get_ressources() == ressources







