from schul_cloud_url_crawler import fetch



def test_fetch_resource(resource, resource_url):
    """Fetch a resource."""
    result = fetch(resource_url)
    assert result.get_resources() == [resource]


def test_fetch_resources(resources, resource_urls):
    """Test that fetching works for a list of resources."""
    result = fetch(resource_urls)
    assert result.get_resources() == resources


def test_fetch_list_of_urls(resources, resource_urls_url):
    """Fetch a document which contains a list of urls."""
    result = fetch(resource_urls_url)
    assert result.get_resources() == resources


def test_there_are_as_many_resources_as_urls(resources, resource_urls):
    """This is a test test: there should be as many resources as urls.

    The urls point to the resources in this order.
    """
    assert len(resources) == len(resource_urls)


def test_make_sure_all_resources_are_crawled_from_list(resource_urls):
    """Test that there is a correlation between urls and cawled content."""
    result = fetch(resource_urls)
    assert len(resource_urls) == len(result.crawled_resources)

def test_make_sure_all_resources_are_crawled_from_url(resource_urls, resources):
    """Test that there is a correlation between urls and cawled content."""
    result = fetch(resource_urls)
    assert len(resource_urls) == len(result.crawled_resources)


def test_crawled_resources(resources, resource_urls):
    """Test that the resources match."""
    result = fetch(resource_urls)
    for i, crawled_resource in enumerate(result.crawled_resources):
        assert crawled_resource.crawled_resource == resources[i]
        assert crawled_resource.origin_urls == [resource_urls[i]]


def test_index_in_urls(resource_urls_url, resource_urls):
    """Test that the resource urls url is inside the origin."""
    result = fetch(resource_urls_url)
    for i, crawled_resource in enumerate(result.crawled_resources):
         expected_origin_urls = [resource_urls_url + "#" + str(i), resource_urls[i]]
         assert crawled_resource.origin_urls == expected_origin_urls


def test_fetch_with_callback(resource_urls, resources):
    """Test that a resource can be passed to fetch."""
    callback_resources = []
    callback = callback_resources.append
    fetch(resource_urls, callback)
    assert resources == [cr.crawled_resource for cr in callback_resources]


class TestRelativeId:
    """When a resource is crawled, it should get its individual id.
    
    This id iscomputed from the index in the file the resource is from.
    """

    def test_only_one_resource_has_no_id(self, resource_urls):
        """If there is only one resource, no id is needed to identify it."""
        result = fetch(resource_urls)
        assert all(not cr.id_in_origin for cr in result.crawled_resources)
    
    def test_the_index_is_added_to_the_ids(self, resources, resource_urls_url):
        result = fetch(resource_urls_url)
        for i in range(len(resources)):
            expected_id = "." + str(i)
            assert result.crawled_resources[i].id_in_origin == expected_id
        





