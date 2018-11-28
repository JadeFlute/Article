import hashlib


def get_md5(url):
    if isinstance(url,str):
        url = url.encode('utf-8')
    url_md5 = hashlib.md5(url).hexdigest()
    return url_md5





























