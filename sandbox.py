import urllib3

def internet_on():
    http = urllib3.PoolManager()
    try:
        r = http.request('GET', 'http://216.58.192.142')
        print("{} is the status of Google".format(r.status))
        return True
    except urllib3.exceptions.MaxRetryError:
        print("Internet is down")
        return False



internet_on()