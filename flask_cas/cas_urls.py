"""
flask_cas.cas_urls

Functions for creating urls to access CAS.
"""

import urllib
import urlparse

def create_url(base, path=None, *query):
    """ Create a url.
    
    Creates a url by combining base, path, and the query's list of 
    key/value pairs. Escaping is handled automatically. Any 
    key/value pair with a value that is None is ignored.

    Keyword arguments:
    base -- The left most part of the url (ex. http://localhost:5000).
    path -- The path after the base (ex. /foo/bar).
    query -- A list of key value pairs (ex. [('key', 'value')]).
    
    Example usage:
    >>> create_url(
    ...     'http://localhost:5000',
    ...     'foo/bar',
    ...     ('key1', 'value'),
    ...     ('key2', None),     # Will not include None
    ...     ('url', 'http://example.com'),
    ... )
    'http://localhost:5000/foo/bar?key1=value&url=http%3A%2F%2Fexample.com'
    """
    url = base
    # Add the path to the url if its not None.
    if path is not None:
        url = urlparse.urljoin(url, urllib.quote(path))
    # Remove key/value pairs with None values.
    query = filter(lambda (k,v): v is not None, query)
    # Add the query string to the url
    url = urlparse.urljoin(url, '?{}'.format(urllib.urlencode(query)))
    return url

def create_cas_login_url(cas_url, service, renew=None, gateway=None):
    """ Create a CAS login URL.

    Keyword arguments:
    cas_url -- The url to the CAS (ex. http://sso.pdx.edu)
    service -- (ex.  http://localhost:5000/login)
    renew -- "true" or "false"
    gateway -- "true" or "false"

    Example usage:
    >>> create_cas_login_url(
    ...     'http://sso.pdx.edu',
    ...     'http://localhost:5000',
    ... )
    'http://sso.pdx.edu/cas?service=http%3A%2F%2Flocalhost%3A5000'
    """
    return create_url(
        cas_url,
        '/cas',
        ('service', service),
        ('renew', renew),
        ('gateway', gateway),
    )

def create_cas_logout_url(cas_url, url=None):
    """ Create a CAS logout URL.

    Keyword arguments:
    cas_url -- The url to the CAS (ex. http://sso.pdx.edu)
    url -- (ex.  http://localhost:5000/login)

    Example usage:
    >>> create_cas_logout_url(
    ...     'http://sso.pdx.edu',
    ...     'http://localhost:5000',
    ... )
    'http://sso.pdx.edu/cas/logout?url=http%3A%2F%2Flocalhost%3A5000'
    """
    return create_url(
        cas_url,
        '/cas/logout',
        ('url', url),
    )

def create_cas_validate_url(cas_url, service, ticket, renew=None):
    """ Create a CAS validate URL.

    Keyword arguments:
    cas_url -- The url to the CAS (ex. http://sso.pdx.edu)
    service -- (ex.  http://localhost:5000/login)
    ticket -- (ex. 'ST-58274-x839euFek492ou832Eena7ee-cas')
    renew -- "true" or "false"

    Example usage:
    >>> create_cas_validate_url(
    ...     'http://sso.pdx.edu',
    ...     'http://localhost:5000/login',
    ...     'ST-58274-x839euFek492ou832Eena7ee-cas'
    ... )
    'http://sso.pdx.edu/cas/validate?service=http%3A%2F%2Flocalhost%3A5000%2Flogin&ticket=ST-58274-x839euFek492ou832Eena7ee-cas'
    """
    return create_url(
        cas_url,
        '/cas/validate',
        ('service', service),
        ('ticket', ticket),
        ('renew', renew),
    )
