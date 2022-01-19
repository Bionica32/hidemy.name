import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from threading import Thread, active_count
import time
heards = { "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.15.146.941 Safari/537.36"}
http = [];https = [];socks4 = [];socks5 = []
def proxy_grabber():
    max_page = max_page_grabber()
    page = [a * 64 for a in range(1, max_page + 1)]
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
    print(f"http: {len(http)}\nsocks4: {len(socks4)}\nsocks5: {len(socks5)}\nThe result is saved in the \"results\" folder")
def max_page_grabber():
    url = "https://hidemy.name/ru/proxy-list/#list"
    r = requests.get(url=url, headers=heards)
    soup = BeautifulSoup(r.text, "lxml")
    max_page = soup.find("li", class_="next_array").find_previous().text
    max_page = int(max_page)
    print(f"Total Pages: {max_page}")
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
def main():
    while active_count() > 400:
        time.sleep(.1)
    Thread(target=proxy_grabber).start()
if __name__ == '__main__':
    main()