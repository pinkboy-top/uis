import threading
import queue
import time
import datetime

import requests

api = "https://duankou.wlphp.com/api.php"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "authority": "duankou.wlphp.com",
    "method": "POST",
    "path": "/api.php",
    "scheme": "https",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "servername=222.179.134.199",
    "origin": "https://duankou.wlphp.com",
    "referer": "https://duankou.wlphp.com/",
    "sec-ch-ua": '"Google Chrome";v="104", "Not)A;Brand";v="8", "Chromium";v="104"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "x-requested-with": "XMLHttpRequest"
}

prox = {
    "https": "127.0.0.1:7890"
}

result = []


def scan_port(port):

    data = {
        "i": "222.179.134.199",
        "p": "{}".format(port)
    }

    req = requests.post(api, headers=headers, proxies=prox, data=data, timeout=10).json()
    if req:
        result.append(req.get("msg"))

    # print(result)


q = queue.Queue()
for x in range(20, 100):
    q.put(str(x))


def start():
    while True:
        if q.empty():
            break
        p = q.get()
        scan_port(p)


if __name__ == '__main__':
    # start_time = time.time()
    # t = threading.Thread(target=start)
    # t1 = threading.Thread(target=start)
    # t2 = threading.Thread(target=start)
    # t3 = threading.Thread(target=start)
    #
    # t.start()
    # t1.start()
    # t2.start()
    # t3.start()
    #
    # t.join()
    # t1.join()
    # t2.join()
    # t3.join()
    # print(result)
    # print(time.time() - start_time)
    start_date = datetime.date(2022, 9, 19)
    end_date = datetime.date(2022, 12, 10)

    print(end_date - start_date)
