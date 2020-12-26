import wxpy


# 微信网页登陆
bot = wxpy.Bot(console_qr=2, cache_path='botoo.pkl')


# 给朋友发送消息
def send_msg():
    # 添加朋友微信昵称
    print(bot.friends())
    friend = bot.friends().search(u'xxxxx')[0]
    friend.send("AAA")


if __name__ == '__main__':
    send_msg()
