visited_urls = set()

def track_url(url):
    """ Add a URL to the set of visited URLs. """
    visited_urls.add(url)

def is_url_visited(url):
    """ Check if a URL has already been visited. """
    return url in visited_urls
