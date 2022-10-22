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
from user.utils.basic import verify_token, save_msg, get_payload

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
    logger.info(f"用户:{account}上线")
    if account not in [x.get("account") for x in login_status]:
        login_status.append({"account": account, "socket_obj": websocket})
    else:
        login_obj = [x for x in login_status if x.get("account") == account][0]

        # 更新websocket对象
        login_obj.update({"account": account, "socket_obj": websocket})

    # 将发送的信息做处理
    # try:
        async for message in websocket:

            logger.info(message)
            res = json.loads(message)

            # 对应的聊天ID
            chat_id = res.get("chat_id")
            # 发送信息的用户ID
            uid = res.get("uid")
            # 发送信息的用户头像
            post_user_avatar = res.get("post_user_avatar")
            # 接收用户的账号
            to_user_account = res.get("to_user_account")
            # 信息绑定的用户
            bind_user_uid = res.get("bind_user_uid")

            login_ids = [x.get("account") for x in login_status]
            msg = res.get("msg")
            now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 将退出用户的状态删除
            exit_page = res.get("exit_page")
            if exit_page:
                for index, item in enumerate(login_status):
                    if item.get("account") == account:
                        login_status.pop(index)
                        break
                logger.info(f"用户:{account}下线")
                continue

            if account in login_ids and to_user_account in login_ids:
                # 把信息发送给接收用户
                logger.info(f"在线用户:{account}==={to_user_account}")
                await save_msg(msg, uid, chat_id, is_read=True)
                socket_obj = [x.get("socket_obj") for x in login_status if x.get("account") == to_user_account][0]

                send_data = {"bind_user_uid": bind_user_uid, "bind_user_avatar": post_user_avatar, "msg": msg, "send_date": now_date}
                await socket_obj.send(
                    json.dumps([send_data]))
            else:
                # 如果用户不在线就先将消息存到队列，等上线后再发送
                await save_msg(msg, uid, chat_id)

    # except Exception as e:
    #     logger.error("websocket异常{}".format(e))


async def main():
    async with serve(recv_msg, "localhost", 6868, ping_interval=60, ping_timeout=5):
        await asyncio.Future()  # run forever


asyncio.run(main())
