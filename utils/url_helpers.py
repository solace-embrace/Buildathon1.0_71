
#===== utils/url_helpers.py =====
from urllib.parse import urlparse
import re

def extract_domain(url):
    try:
        d = urlparse(url)
        host = d.netloc if d.netloc else d.path.split("/")[0]
        return host.lower()
    except Exception:
        return ""

def extract_path(url):
    try:
        d = urlparse(url)
        return d.path + ("?" + d.query if d.query else "")
    except Exception:
        return ""

def has_raw_ip(domain):
    # Returns True if domain is IPv4, e.g. 8.8.8.8
    m = re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain)
    return m is not None
