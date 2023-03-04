# Site used to get proxies is below geonode provide direct json,txt,csv of all ips
# https://geonode.com/free-proxy-list
# it also gives direct link to load
import requests
import json
proxy_url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
target_url = "http://httpbin.org/ip"


def fetchproxy(url):
    data = requests.get(url)
    json_data = json.loads(data.text)
    proxies = list()
    for i in range(0, len(json_data["data"])):
        proxy = json_data["data"][i]["ip"] + \
            str(":") + json_data["data"][i]["port"]
        proxies += [{'http': 'http://' + proxy}]
    return proxies


def send_request(proxies):
    for proxy in proxies:
        try:
            response = requests.get(target_url,
                                    proxies=proxy, timeout=3)
            print("Working Proxy : " + response.json()["origin"])
        except:
            pass


def main():
    proxies = fetchproxy(proxy_url)
    send_request(proxies)


if __name__ == "__main__":
    main()
