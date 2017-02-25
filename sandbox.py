import urllib

def check_connectivity():
    try:
        urllib.request.urlopen("http://216.58.192.142", timeout=1)
        return True
    except urllib.request.URLError:
        return False

