import httpx
from httpx_socks import SyncProxyTransport
from threading import Thread, active_count
from tqdm import tqdm
import time
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
if __name__ == '__main__':
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
