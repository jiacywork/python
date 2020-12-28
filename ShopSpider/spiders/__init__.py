import time
import datetime

while 1:
    # 开始登录并进入购物车
    if '16:10:00.000' in str(datetime.datetime.now()):
        print(datetime.datetime.now())
        time.sleep(1)
    # 整点开始下单
    elif '16:10:30.000' in str(datetime.datetime.now()):
        print(datetime.datetime.now())
        break
    else:
        time.sleep(0.000001)
