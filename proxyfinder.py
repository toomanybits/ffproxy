# Site used to get proxies is below geonode provide direct json,txt,csv of all ips
# https://geonode.com/free-proxy-list
# it also gives direct link to load
import requests
import json
import csv
proxy_url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
# site to check whether proxy working returns ip dictionary
target_url = "http://httpbin.org/ip"

# function created to return proxy list from geonode json data


def fetchproxy(url):
    data = requests.get(url)
    json_data = json.loads(data.text)
    proxies = list()
    # adding basic format of proxy
    for i in range(0, len(json_data["data"])):
        proxy = json_data["data"][i]["ip"] + \
            str(":") + json_data["data"][i]["port"]
        proxies.append(proxy)
    return proxies

# function created to ping target url and find the working one


def send_request(proxies):
    workingproxies = list()
    for proxy in proxies:
        try:
            # will send request to httpbin using proxy from fetched proxies
            response = requests.get(target_url,
                                    # adding basic schema of proxy
                                    proxies={'http': 'http://' + proxy,
                                             'https': 'https://' + proxy},
                                    timeout=3)
            print("Working Proxy : " + response.json()["origin"])
            # will add working proxy to workingproxylist
            workingproxies.append(proxy)
        except:
            print("Failed Proxy : " + proxy)
            pass
        return workingproxies

# for export working proxies as a csv file


def export(proxylist):
    with open("workingproxy.csv", "w", newline="", encoding="UTF-8") as f:
        # loop for witing each row in csv
        for proxy in proxylist:
            f.write(proxy + "\n")


def main():
    proxies = fetchproxy(proxy_url)
    working = send_request(proxies)
    export(working)


if __name__ == "__main__":
    main()
