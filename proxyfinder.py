# Site used to get proxies is below geonode provide direct json,txt,csv of all ips
# https://geonode.com/free-proxy-list
# it also gives direct link to load
import requests
import json
import concurrent.futures
print("Remember a larger number might help to find more working proxy but will consume more resources and time")
try:
    n = int(input("How Many Proxies You Want To Search For : "))
except:
    print("Enter a valid number")

proxy_url = f"https://proxylist.geonode.com/api/proxy-list?limit={n}&page=1&sort_by=lastChecked&sort_type=desc&protocols=http"
# site to check whether proxy working returns ip dictionary
target_url = "http://httpbin.org/ip"
working = list()

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


def send_request(proxy):
    try:
        # will send request to httpbin using proxy from fetched proxies
        response = requests.get(target_url,
                                # adding basic schema of proxy
                                proxies={'http': 'http://' + proxy,
                                         'https': 'https://' + proxy},
                                timeout=3)
        print("Working Proxy : " + str(response.json()["origin"]))
        # will add working proxy to workingproxylist
        working.append(proxy)
    except:
        pass

# for export working proxies as a csv file


def export(proxylist):
    with open("workingproxy.csv", "w", newline="", encoding="UTF-8") as f:
        # loop for witing each row in csv
        for proxy in proxylist:
            f.write(proxy + "\n")


def main():
    proxies = fetchproxy(proxy_url)
    # using concurrent future to send all requests and wait in parrallel for response
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(send_request, proxies)
    export(working)


if __name__ == "__main__":
    main()
