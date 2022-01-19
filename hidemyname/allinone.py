import requests
from bs4 import BeautifulSoup
import httpx
from httpx_socks import SyncProxyTransport
from threading import Thread, active_count
from tqdm import tqdm
import time
import os
import sys
heards = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.15.146.941 Safari/537.36"}
http = [];https = [];socks4 = [];socks5 = []
def proxy_grabber():
    max_page = max_page_grabber()
    page = [a * 64 for a in range(1, max_page + 1)]
    # page = [a * 64 for a in range(1, 1 + 1)]
    for num in tqdm(page):
        r = requests.get(url=f"https://hidemy.name/ru/proxy-list/?start={num}#list", headers=heards)
        soup = BeautifulSoup(r.text, "lxml")
        for tr in soup.find("tbody").find_all("tr"):
            card = [x.text for x in tr.find_all("td")]
            ptype = str(card[4]).lower()
            proxy = f"{ptype}:{card[0]}:{card[1]}"
            if card[4] == "HTTP": http.append(proxy)
            if card[4] == "HTTPS": http.append(proxy)
            if card[4] == "SOCKS4": socks4.append(proxy)
            if card[4] == "SOCKS5": socks5.append(proxy)
    txt_saver()
    print(f"http: {len(http)}  socks4: {len(socks4)}  socks5: {len(socks5)}")
def max_page_grabber():
    url = "https://hidemy.name/ru/proxy-list/#list"
    r = requests.get(url=url, headers=heards)
    soup = BeautifulSoup(r.text, "lxml")
    max_page = soup.find("li", class_="next_array").find_previous().text
    max_page = int(max_page)
    print(f"Total pages: {max_page}")
    time.sleep(0.5)
    return max_page
def txt_saver():
    if os.path.exists("results"):
        with open("results/http.txt", "w") as file:
            for line in http:
                line = line + "\n"
                file.write(line)
        with open("results/socks4.txt", "w") as file:
            for line in socks4:
                line = line + "\n"
                file.write(line)
        with open("results/socks5.txt", "w") as file:
            for line in socks5:
                line = line + "\n"
                file.write(line)
    else:
        os.mkdir("results")
        with open("results/http.txt", "w") as file:
            for line in http:
                line = line + "\n"
                file.write(line)
        with open("results/socks4.txt", "w") as file:
            for line in socks4:
                line = line + "\n"
                file.write(line)
        with open("results/socks5.txt", "w") as file:
            for line in socks5:
                line = line + "\n"
                file.write(line)
def check():
    check_input = input("Which proxy type need to check? (1 - http(s), 2 - socks4, 3 - socks5, Enter - all): ")
    if check_input == "1":
        check = ['http']
    else:
        if check_input == "2":
            check = ['socks4']
        else:
            if check_input == "3":
                check = ['socks5']
            else:
                if check_input == "":
                    check = ['http', 'socks4', 'socks5']
                else:
                    check = "incorrect"
    return check
def site():
    site = input("Which website to check? (Enter to use httpbin.org): ")
    if site == "":
        site = "httpbin.org"
    return site
    print(f"Website to check: {site}")
def pisos(url):
    try:
        transport = SyncProxyTransport.from_url(url)
        with httpx.Client(transport=transport) as client:
            try:
                res = client.get(f"http://{site}", timeout=timeout)
                good.append(url.strip(f'{type}://'))
            except:
                pass
    except:
        pass
def main():
    proxy_grabber()
def end():
    print("Done!")
if __name__ == '__main__':
    main()
    site = site()
    doc = check()
    timeout = input("Maximum check timeout: (Enter - 1024): ")
    if timeout == "":
        timeout = 1024
    else:
        timeout = int(timeout)
    if len(doc) < 4:
        for a in doc:
            file = f"results/{a}.txt"
            good = []
            with open(file, "r") as f:
                f_lines = f.readlines()
                for line in tqdm(f_lines):
                    line = str(line)
                    line = line.strip('\n')
                    proxy = f"{line.split(':')[1]}:{line.split(':')[2]}"
                    type = line.split(':')[0]
                    while active_count() > 256:
                        time.sleep(.1)

                    Thread(target=pisos, args=[f"{type}://{proxy}"]).start()
                print(f"Found good {type}: {len(good)}/{len(f_lines)}")
                time.sleep(0.5)



        if os.path.exists("goods"):
            with open(f"goods/{a}.txt", "a") as file:
                for item in good:
                    item = item + "\n"
                    file.write(item)
        else:
            os.mkdir("goods")
            with open(f"goods/{a}.txt", "a") as file:
                for item in good:
                    item = item + "\n"
                    file.write(item)

    else:
        print("Incorrect input...")