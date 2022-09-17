import queue
import threading

import requests

api = "https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&rank_time=34&rank_role=1&skin=1"
token = None
q = queue.Queue()
prox = {
    "https": "127.0.0.1:7890"
}


def post():
    if token:
        header = {
            "Host": "cat-match.easygame2021.com",
            "Connection": "keep-alive",
            "xweb_xhr": "1",
            "t": "{}".format(token),
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wx141bfb9b73c970a9/15/index.html",
            "Accept-Language": "en-us,en",
            "Accept-Encoding": "gzip, deflate"
        }

        if prox:
            req = requests.get(api, headers=header, proxies=prox, verify=False).json()
        else:
            req = requests.get(api, headers=header, verify=False).json()

        if req.get("data") == 0:
            print("通关成功")


def main():
    while True:
        if q.empty():
            break
        p = q.get()
        post()


if __name__ == '__main__':

    print("===输入抓包获取的token和通关的次数===")

    token = input("请输入token:")
    number = input("请输入通关次数:")

    if token and number:
        try:
            for i in range(int(number)):
                q.put(i)

            threads = []
            for _ in range(4):
                t = threading.Thread(target=main)

                threads.append(t)
                t.start()

            for t in threads:
                t.join()
        except Exception as e:
            print(e)
