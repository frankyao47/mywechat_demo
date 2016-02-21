#/usr/bin/env python
#coding: utf-8

from wechat_sdk import WechatConf, WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage

conf = WechatConf(
    token='wechatTest', 
    appid='wxf3a6719e17c64426', #appID
    appsecret='a7514c12127ddd7268c927215527782f', #appsecret
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='53B5F3E270C7C1DF99DCC9B55FC83C31'  # 如果传入此值则必须保证同时传入 token, appid
)

# conf = WechatConf(
#     token='wechatTest', 
#     appid='wx1eac638bf2f26cc5', #appID
#     appsecret='b852fca1e60196f412afb2f51cb2019b', #appsecret
#     encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
#     encoding_aes_key='k52No4Iae1PIzjwxsma4EDcWo210CfdaEOtc3SuTGsu'  # 如果传入此值则必须保证同时传入 token, appid
# )


wechat = WechatBasic(conf=conf)

from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET': #validate
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        if wechat.check_signature(signature, timestamp, nonce):
            return echostr
    else: #XML message
        try:
            wechat.parse_data(request.data)
            wid = wechat.message.id          # 对应于 XML 中的 MsgId
            wtarget = wechat.message.target  # 对应于 XML 中的 ToUserName
            wsource = wechat.message.source  # 对应于 XML 中的 FromUserName
            wtime = wechat.message.time      # 对应于 XML 中的 CreateTime
            wtype = wechat.message.type      # 对应于 XML 中的 MsgType
            wraw = wechat.message.raw        # 原始 XML 文本，方便进行其他分析

            if isinstance(wechat.message, TextMessage): #TextMessage
                wcontent = wechat.message.content
                wresponse = wechat.response_text(content=wcontent)
                return wresponse
            else:
                pass   
        except ParseError:
            pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)