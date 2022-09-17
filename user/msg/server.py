import os
import django
import asyncio
import datetime
import json
import queue
import sys

from websockets import serve


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uis.settings')
django.setup()


from uis.settings import logger
from user.utils.basic import verify_token, save_msg, get_msg, get_payload

# 保存用户登录状态
login_status = []


# 接收客户端消息并处理
async def recv_msg(websocket):
    token = websocket.path.split("token=")[-1]

    # 验证token是否过期
    if verify_token(b'pink-boy', token):
        now_time = datetime.datetime.now()
        flag_time = get_payload(token).get("exp")
        exp_time = datetime.datetime.fromtimestamp(flag_time)
        if now_time > exp_time:
            await websocket.close(1011, "登录已过期！")
            return
    else:
        await websocket.close(1011, "未登录！")
        return

    # 将account和socket放到登录信息
    account = get_payload(token).get("data").get("account")
    if account not in [x.get("account") for x in login_status]:
        login_status.append({"account": account, "socket_obj": websocket})
    else:
        login_obj = [x for x in login_status if x.get("account") == account][0]

        # 更新websocket对象
        login_obj.update({"account": account, "socket_obj": websocket})

    # 将发送的信息做处理
    # try:
        async for message in websocket:

            # print(message)
            res = json.loads(message)

            # 检查接收用户是否登录，没有登录就放到消息队列里面，登录了就发送给对应的用户
            chat_id = res.get("chat_id")
            to_user = res.get("to_user")
            send_user = res.get("send_user")
            login_ids = [x.get("account") for x in login_status]
            msg = res.get("msg")
            now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 用户打开页面的时候将历史信息发送
            open_page = res.get("open_page")
            if open_page:
                history_msg = await get_msg(chat_id)
                await websocket.send(json.dumps(history_msg))

            # 将退出用户的状态删除
            exit_page = res.get("exit_page")
            if exit_page:
                for index, item in enumerate(login_status):
                    if item.get("account") == send_user:
                        login_status.pop(index)
                        break
                print(f"用户:{account}下线")
                continue

            if to_user in login_ids and send_user in login_ids:
                # 将对应的消息发送给对应的用户
                print("都在线")
                socket_obj = [x.get("socket_obj") for x in login_status if x.get("account") == to_user][0]
                await socket_obj.send(
                    json.dumps([{"to_user": to_user, "send_user": send_user, "msg": msg, "send_date": now_date}]))
            if msg:
                # 如果用户不在线就先将消息存到队列，等上线后再发送
                await save_msg(msg, chat_id)

    # except Exception as e:
    #     logger.error("websocket异常{}".format(e))


async def main():
    async with serve(recv_msg, "localhost", 6868, ping_interval=60, ping_timeout=5):
        await asyncio.Future()  # run forever


asyncio.run(main())
