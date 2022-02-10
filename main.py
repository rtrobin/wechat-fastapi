from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
import requests
import re
import asyncio
import os

from wechatpy.enterprise import parse_message, create_reply
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException

app = FastAPI()
TOKEN = os.environ.get('TOKEN', '')
AES_KEY = os.environ.get('AESKEY', '')
CORP_ID = os.environ.get('CORPID', '')

@app.get('/wechat')
async def wechat(
    msg_signature: str,
    timestamp: str,
    nonce: str,
    echostr: str
):
    crypto = WeChatCrypto(TOKEN, AES_KEY, CORP_ID)
    try:
        echostr = crypto.check_signature(
            msg_signature,
            timestamp,
            nonce,
            echostr
        )
    except InvalidSignatureException:
        raise HTTPException(status_code=403)

    return HTMLResponse(content=echostr)

async def fetch_info(msg: str) -> str :
    msg = msg.lower()

    def parse_url(url: str, type: str) -> str:
        full_text = requests.get(url).content.decode()
        links = re.findall(f'{type}://.+(?=</)', full_text)

        ret = ''
        for link in links:
            ret += link + '\n'
        return ret[:-1]

    if msg == 'vmess':
        url = 'https://github.com/Alvin9999/new-pac/wiki/v2ray免费账号'
    elif msg == 'ss' or msg == 'ssr':
        url = 'https://github.com/Alvin9999/new-pac/wiki/ss免费账号'
    else:
        return '暂不支持(⊙_⊙)?'

    return await asyncio.to_thread(parse_url, url, msg)

@app.post('/wechat')
async def wechat(
    msg_signature: str,
    timestamp: str,
    nonce: str,
    body_msg: str = Body(..., media_type='application/html')
):
    crypto = WeChatCrypto(TOKEN, AES_KEY, CORP_ID)
    try:
        body_msg = crypto.decrypt_message(
            body_msg,
            msg_signature,
            timestamp,
            nonce
        )
    except (InvalidSignatureException, InvalidCorpIdException):
        raise HTTPException(status_code=403)
    else:
        msg = parse_message(body_msg)
        if msg.type != 'event':
            reply = create_reply('暂不支持该类型_(:зゝ∠)_', msg)
        else:
            reply = await fetch_info(msg.key)
            reply = create_reply(reply, msg)
        return HTMLResponse(crypto.encrypt_message(reply.render(), nonce, timestamp))

    